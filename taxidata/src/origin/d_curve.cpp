#include <iostream>
#include <stdio.h>
#include <math.h>
#include "vector"
#include "thread"

#ifndef DCURVE_H
#define DCURVE_H

//windows용 전처리 구문 dll 파일을 만들때 함수를 잘 내보내기 위한 코드
// 리눅스에서는 쓸모 없음.
#define DCURVE_API __declspec(dllexport)

#ifdef __cplusplus
extern "C" {
#endif

    DCURVE_API float d_pp(float x1, float y1, float x2, float y2);
    DCURVE_API float d_ls_p(float* line_points, int line_length, float px, float py, int line_start = 0);
    DCURVE_API float d_curve_single(float* seg_points, int seg_length, float* traj_points, int traj_length, int index, int seg_index, float& prefix, int seg_start = 0);
    DCURVE_API void d_curve(float* segments, int* segment_lengths, int* segment_start_point, int total_seg_num, float* traj_points, int traj_length, int index, float* prefix, float* d_c, int thr_num = 1);

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


#endif

