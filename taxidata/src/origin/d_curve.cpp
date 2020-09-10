#include <iostream>
#include <fstream>
#include <stdio.h>
#include <math.h>
#include <string>
#include "vector"
#include "thread"
#include <cassert>
#include <algorithm>

//compile option 
//g++ -DDLINUX -std=c++17 -shared -fPIC -O2 -o d_curve.so.1 -c origin/d_curve.cpp 

#ifndef DCURVE_H
#define DCURVE_H

//windows용 전처리 구문 dll 파일을 만들때 함수를 잘 내보내기 위한 코드
// 리눅스에서는 쓸모 없음.
#ifndef DLINUX
#define DCURVE_API __declspec(dllexport)
#else
#define DCURVE_API
#endif

#ifdef __cplusplus
extern "C" {
#endif

    DCURVE_API float d_pp(float x1, float y1, float x2, float y2);
    DCURVE_API float d_ls_p(float* line_points, int line_length, float px, float py, int line_start = 0);
    DCURVE_API float d_curve_single(float* seg_points, int seg_length, float* traj_points, int traj_length, int index, int seg_index, float& prefix, int seg_start = 0);
    DCURVE_API void d_curve(float* segments, int* segment_lengths, int* segment_start_point, int total_seg_num, float* traj_points, int traj_length, int index, float* prefix, float* d_c, int thr_num = 1);
    //DCURVE_API void k_segment_single(ofstream* file, int* edges, int* edge_start_indices, int* degrees, int total_number, int start_node, float* length, float* angle, float k);
    DCURVE_API void k_segments(int* edges, int* edge_start_indices, int* degrees, int total_number, int* start_node, int n_num, float* length, float* angle, float k, int thr_num = 1);

#ifdef __cplusplus
};
#endif

using  namespace std;

//distance point and point
float d_pp(float x1, float y1, float x2, float y2)
{
    return sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2));
}

//!function distance between line and point
// line = [l1(x,y), l2(x,y)] , point = [px, py]
// this will make d_curve
float d_l_p(float l1x, float l1y, float l2x, float l2y, float px, float py) {
    float a = l2y - l1y;
    float b = l1x - l2x;

    float shortest = fabs(a * px + b * py - a * l1x - b * l1y) / sqrtf(a * a + b * b);

    float m1 = -a / (b + 1e-9);
    float m2 = -1. / (m1 + 1e-9);

    float x = (m1 * l1x - m2 * px - l1y + py) / (m1 - m2);
    float y = m2 * (x - px) + py;

    float cdot = (l1x - x) * (l2x - x) + (l1y - y) * (l2y - y);
    if (cdot <= 0) {
        return shortest;
    }
    else {
        float l1 = d_pp(l1x, l1y, px, py);
        float l2 = d_pp(l2x, l2y, px, py);

        return (l1 > l2) ? l2 : l1;
    }
}

//!function : euclidian distance between line and point
//line_length : n
//line_points : [l1x, l1y, l2x, l2y, l3x, l3y, ... , lnx, lny]
//calculation is iterably done by line points, and return minimum distance.
float d_ls_p(float* line_points, int line_length, float px, float py, int line_start) {
    float dis_min = 1e12;
    for (size_t i = 0; i < line_length - 1; i++)
    {
        float result = d_l_p(line_points[line_start + 2 * i], line_points[line_start + 2 * i + 1], line_points[line_start + 2 * i + 2], line_points[line_start + 2 * i + 3], px, py);
        if (result < dis_min)
        {
            dis_min = result;
        }

    }
    return dis_min;
}


//!function : calculation of d_curve using prefix.
//input :
//  length : n
//  points : [l1x, l1y, l2x, l2y, l3x, l3y, ... , lnx, lny]
//output :
// d_curve.
float d_curve_single(float* seg_points, int seg_length, float* traj_points, int traj_length, int index, int seg_index, float& prefix, int seg_start) {
    float seg_traj_distance;
    ///////////////////// if the calculation has been done before, we will re-use that result for this calculation 
    ///////////////////// in that case, we will save the time for n-iter calcuation 
    if (!prefix) {
        seg_traj_distance = 0;
        for (size_t i = 0; i < seg_length; i++)
        {
            float result = d_ls_p(traj_points, traj_length, seg_points[seg_start + 2 * i], seg_points[seg_start + 2 * i + 1]);
            if (result > seg_traj_distance) {
                seg_traj_distance = result;
            }
        }
        prefix = seg_traj_distance;
    }
    else {
        seg_traj_distance = prefix;
    }

    float closest = d_ls_p(seg_points, seg_length, traj_points[2 * index], traj_points[2 * index + 1]);

    return (closest > seg_traj_distance) ? closest : seg_traj_distance;
}

void thread_d_c(float* segments, int* segment_lengths, int* segment_start_point, int start, int end, float* traj_points, int traj_length, int index, float* prefix, float* d_c) {
    for (size_t i = start; i < end - start; i++)
    {
        d_c[i] = d_curve_single(segments, segment_lengths[i], traj_points, traj_length, index, i, prefix[i], segment_start_point[i]);
    }
}

void d_curve(float* segments, int* segment_lengths, int* segment_start_point, int total_seg_num, float* traj_points, int traj_length, int index, float* prefix, float* d_c, int thr_num) {
    if (thr_num == 1) {
        thread_d_c(segments, segment_lengths, segment_start_point, 0, total_seg_num, traj_points, traj_length, index, prefix, d_c);
        return;
    }
    else {
        vector<thread> workers;

        int unit = total_seg_num / thr_num;
        int remain = total_seg_num % thr_num;
        //distribute work
        for (size_t i = 0; i < thr_num; i++) {
            workers.push_back(thread(thread_d_c, segments, segment_lengths, segment_start_point, i * unit, (i + 1) * unit, traj_points, traj_length, index, prefix, d_c));
        }
        thread_d_c(segments, segment_lengths, segment_start_point, unit * thr_num, total_seg_num, traj_points, traj_length, index, prefix, d_c);
        //gather thread
        for (size_t i = 0; i < thr_num; i++) {
            workers[i].join();
        }
        //printf("join work.\n");
        //메모리 해제
        workers.clear();
        return;
    }

}



void segments_output(ofstream* file, vector<int> segment, int end, vector<float> length, float end_length, float total) {
    for (vector<int>::iterator it = segment.begin(); it != segment.end(); ++it)
    {
        (*file) << *it << ",";
    }
    (*file) << end << endl;
    for (vector<float>::iterator it = length.begin(); it != length.end(); ++it)
    {
        (*file) << *it << ",";
    }
    (*file) << end_length << ", total : " << total + end_length << endl;
}

void k_segment_single(ofstream* file, int* edges, int* edge_start_indices, int* degrees, int total_number, int start_node, float* length, float* angle, float k) {
    

    // dfs tree
    vector< vector <int> >     tree;
    vector< vector <float> >   ltree;
    vector< vector <float> >   atree;

    // segment object
    vector <int>   current_segment;
    vector <float> segment_length;
    vector <float> segment_angle;
    current_segment.push_back(start_node);
    current_segment.push_back(0);  // dummy node.
    segment_length.push_back(0);
    segment_angle.push_back(0);
    segment_angle.push_back(0);

    // node and length
    int next_node;
    float next_len;
    float next_angle;
    float d_angle;
    float orientation = 100;
    float current_length = 0;
    float current_angle = 0;

    // layer of tree
    vector<int> layer;
    vector<float> len_layer;
    vector<float> ang_layer;

    // initialize
    for (size_t i = 0; i < degrees[start_node]; i++)
    {
        next_node = edges[(edge_start_indices[start_node] + i) * 3 + 1];
        if (edges[(edge_start_indices[start_node] + i) * 3 + 2] == 1) {
            next_node *= -1;
        }
        layer.push_back(next_node);
        len_layer.push_back(length[edge_start_indices[start_node] + i]);
        ang_layer.push_back(angle[edge_start_indices[start_node] + i]);
    }
    tree.push_back(layer);
    ltree.push_back(len_layer);
    atree.push_back(ang_layer);
    layer.clear();
    len_layer.clear();
    ang_layer.clear();
    int ch = 0;
    // main loop
    while (true)
    {
        ch++;
        // ascendent
        while (layer.empty())
        {
            if (tree.empty())
            {
                return;
            }


            current_segment.pop_back();
            current_length -= segment_length.back();
            segment_length.pop_back();

            layer = tree.back();
            len_layer = ltree.back();
            ang_layer = atree.back();
            tree.pop_back();
            ltree.pop_back();
            atree.pop_back();
            if (tree.empty())
            {
                orientation = 100;
                current_angle = 0;
            }
            else {
                d_angle = abs(segment_angle.end()[-2] - segment_angle.end()[-1]);
                d_angle = d_angle = min(d_angle, abs(d_angle - 2 * 3.141592653f));
                current_angle -= d_angle;
            }
            segment_angle.pop_back();

        }
        // decendent
        while (!layer.empty()) {

            current_segment.push_back(layer.back());
            segment_length.push_back(len_layer.back());
            current_length += len_layer.back();
            segment_angle.push_back(ang_layer.back());
            d_angle = abs(segment_angle.end()[-2] - segment_angle.end()[-1]);
            d_angle = d_angle = min(d_angle, abs(d_angle - 2 * 3.141592653f));
            current_angle += d_angle;


            layer.pop_back();
            len_layer.pop_back();
            ang_layer.pop_back();

            vector <int> new_layer;
            vector <float> new_length;
            vector <float> new_angle;
            int c_node = current_segment.back();
            if (c_node < 0) {
                c_node *= -1;
            }
            for (size_t i = 0; i < degrees[c_node]; i++)
            {
                next_node = edges[(edge_start_indices[c_node] + i) * 3 + 1];
                if (edges[(edge_start_indices[c_node] + i) * 3 + 2] == 1) {
                    next_node *= -1;
                }


                next_len = length[edge_start_indices[c_node]+i];
                next_angle = angle[edge_start_indices[c_node]+i];
                d_angle = abs(next_angle - segment_angle.end()[-1]);
                d_angle = min(d_angle, abs(d_angle - 2 * 3.141592653f));


                if (next_node == current_segment.end()[-2]) {
                    assert(d_angle > 3.14);
                }
                if (next_len + current_length > k || (current_angle + d_angle > 3.141592653 * 2)) {
                    segments_output(file, current_segment, next_node, segment_length, next_len, current_length);
                }
                else {
                    new_layer.push_back(next_node);
                    new_length.push_back(next_len);
                    assert(current_angle + d_angle < 3.141592653 * 2);
                    new_angle.push_back(next_angle);
                }
            }
            tree.push_back(layer);
            ltree.push_back(len_layer);
            atree.push_back(ang_layer);

            layer = new_layer;
            len_layer = new_length;
            ang_layer = new_angle;
        }
    }



}

void k_segment_thread(int* edges, int* edge_start_indices, int* degrees, int total_number, int* start_node, int start, int end, float* length, float* angle, float k) {
    /// file system
    string name("k_seg");
    string middle("_");
    string ext(".dat");
    ofstream* file = new ofstream(name + to_string(start_node[start])+ middle + to_string(start_node[end-1]) + ext);
    for (size_t i = start; i < end; i++)
    {
        k_segment_single(file, edges, edge_start_indices, degrees, total_number, start_node[i], length, angle, k);
    }
    file->close();
}

DCURVE_API void k_segments(int* edges, int* edge_start_indices, int* degrees, int total_number, int* start_node, int n_num, float* length, float* angle, float k, int thr_num) {
    if (thr_num == 1) {
        k_segment_thread(edges, edge_start_indices, degrees, total_number, start_node, 0, n_num, length, angle, k);
        return;
    }
    else {
        vector<thread> workers;

        int unit = n_num / thr_num;
        int remain = n_num % thr_num;
        //distribute work
        for (size_t i = 0; i < thr_num; i++) {
            workers.push_back(thread(k_segment_thread, edges, edge_start_indices, degrees, total_number, start_node, i * unit, (i + 1) * unit, length, angle, k));
        }
        k_segment_thread(edges, edge_start_indices, degrees, total_number, start_node, thr_num * unit, n_num, length, angle, k);
        //gather thread
        for (size_t i = 0; i < thr_num; i++) {
            workers[i].join();
        }
        //메모리 해제
        workers.clear();
        return;
    }

}


#endif

