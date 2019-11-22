#taxidata.tdarray.__init__.py
__all__ = ['tdarray']

import numpy as np
#from math import sin, cos, atan2, pi, sqrt  #fast calculation speed
#import profile ,sys                         #profile and get size of variable and function
#from ..taxifiles import taxifiles
from ..core.lib import *
import datetime as dt

class tdarray:
    '''This class is pre-processor for taxi data. This class take DAT files for data, return numpy array.
    So, tdarray needs taxifiles as input and does some processing(i.e. timestamp from string etc.) and make numpy array.
    Cause the data is very big, parsing may occur memory error. Thus, tdarray only can be defined or work one with same time.
    '''
    data = None
    #class member variable
    dtype = [('id','i4'),('x','i4'),('y','i4'),('time',np.uint32),('vel','i4'),('psg',np.bool),('district','i4')]


    def delete(self):
        del tdarray.data
        tdarray.data = None


    #User`s method
    def __init__(self, name, files):
        self.name = name
        self.files = files #taxifiles type
        self.line = 0
        self.error =0

    def construct(self, force_delete = False , line=None):
        if tdarray.data and not force_delete:
            raise ValueError("Data is already occupied. please do method 'delete()'.")
        elif force_delete:
            self.delete()
        if not line:
            line = int(4e8/576*len(self.files))
        tdarray.data = np.zeros([line], dtype=tdarray.dtype)


    def read(self, array=None, log = None, error = None, err_arr = None,delete = False): #log, error must be file, err_arr ndarray
        '''read() method take 1 array, if there is no array than the class '''
        global carte, mapping, timestamp, univ, rotate, linetoarray
        if array is None:
            self.construct(force_delete = True)
            data = tdarray.data
        else:
            data = array

        b_log = False
        b_error = False
        b_arr = False
        print("{} Read Processing...".format(self.name))
        if log is not None and log.writable():
            b_log = True
            print('{} log caught.'.format(self.name))
            log.write("Read taxidata in {}".format(str(self.files)))
        if error is not None and error.writable():
            b_error = True
            print('{} error caught.'.format(self.name))
            error.write("Occured Error when Read taxidata in {}".format(str(self.files)))

        if type(err_arr) == np.ndarray and err_arr.dtype == self.dtype:
            b_arr = True
        print("Total file counts : {}".format(len(self.files)))

        max_line = len(data)
        ch = 0
        files = 0
        totalline = 0
        start_time = dt.datetime.now()
        total_error = 0

        #percentage
        percent = 0


        for file in self.files:
            ########## percent ##########
            print("{}\t\t{}%".format(file.name, percent),end='\r')

            ########## property ##########
            lines = 0
            errors = 0

            ########## log ##########
            if b_log:
                fstart = dt.datetime.now()
                log.write("File number {} :".format(files+1)+self.files.path[files]+" opened. ({})\n".format(fstart.strftime("%y-%m-%d %H:%M:%S")))
                log.flush()
            if b_error:
                error.write("\nerror in {}\n".format(self.files.path[files]))
                error.flush()

            ########## line reading ##########
            for line in file:
                lines += 1
                temp = line.split(",")
                if len(temp[1])<7 or len(temp[2])<7:
                    if b_arr:
                        try:
                            err_arr[(errors+total_error)] = linetoarray(0,0, temp)
                        except:
                            pass
                    if b_error:
                        error.write("\t {}".format(line))
                    errors+=1
                    continue
                else:
                    x, y = mapping(float(temp[2])*1e-7,float(temp[1])*1e-7)
                    data[ch] = linetoarray(x,y, temp)
                    ch+=1

                if ch==max_line:
                    print("process force finished by overflow lines.")
                    return

            ########## merge ##########
            totalline += lines
            total_error += errors
            files+= 1
            if b_log:
                fend = dt.datetime.now()
                ftime = (fend-fstart).seconds
                fm = int(ftime/60)
                ftime = ftime%60
                totaltime = (fend - start_time).seconds
                tm = int(totaltime/60)
                ts = totaltime%60

                log.write("file number {} finished.({})\n\tResult: error : {}/{}, ftime : {}m {}s, cumulate time : {}m {}s\n".format(files, fend.strftime("%y-%m-%d %H:%M:%S"), errors, lines, fm, ftime, tm, ts))
                log.flush()

            #percentage print in loop(for file in self.files)
            percent = int(files/len(self.files)*100)
            if percent == 100:
                print("{}\t\t{}%".format(file.name, percent))

            #every end of file, log of its property time, total time, error line, current line

        print("{} Finished.".format(self.name))
        self.line = ch
        self.total_error = total_error
        if b_log:
            end_time = dt.datetime.now()
            log.write("\nFinished. ({})\nTotal lines : {}, Total error : {}, Final lines : {}, Total time : {}m {}s \ndone.".format(end_time.strftime("%y-%m-%d %H:%M:%S"), totalline, total_error, ch, tm, ts))
            log.close()
            error.close()
        return self.line, self.total_error


    def save(self, name, data = None, err_arr = None, spilt = False):
        if name is None:
            name = self.name
        if data is None:
            data = self.data
        np.save(name , data[:self.line])
        if err_arr is not None:
            e = name.find(".")
            if e>=0:
                error = name[:e]+"e"+name[e:]
            else:
                error = name+"e"
            np.save(error, err_arr[:self.total_error])
