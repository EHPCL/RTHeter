# 
# Copy Right. The EHPCL Authors.
#

import numpy as np

class TaskRandomGenerator:
    """ Task generator with fixed result under same seed. Generate 5 tasks given utilization
    from 1.0 to 4.1+, each with 5 segments [1,5]. The period must be a division of 180.
    """

    def __init__(self, seed) -> None:
        self.tasktype = np.dtype([
            ('period', np.int32),   
            ('task_load', np.int32)
        ])
        self.seed = seed
        np.random.seed(self.seed)
        self.task_data = np.zeros((50, 20 ,5), dtype=self.tasktype)
        self.segment_cuont = 5
        self.task_count = 5
        self.data_init()

    def generate(self, utilization: float) -> 'list[tuple[int, tuple[int]]]':
        """generate according to the uti given, error within 1%

        Returns:
            [task1, task2, ...] \n
            task: (period, (segments)) \n
            segments: (s0, s1, s2, s3, ...) \n
        """
        np.random.seed(self.seed)
        uti_10 = int(utilization * 10)
        task_choice = self.seed%20

        valid = False
        while not valid:
            result = []
            for i in range(self.task_count):
                period, tot = self.task_data[uti_10][task_choice][i]
                if tot == period: break
                result.append((period, self.segmentation(tot)))
            if len(result) == self.task_count: valid = True
            task_choice = (task_choice + 1)%20

        return result

    def segmentation(self, total: int):
        # segment <total> into [1,5]
        result = []
        np.random.seed(self.seed)
        remain = total
        while (len(result) < self.segment_cuont):
            remain_count = self.segment_cuont - len(result)
            upper_bound = min(5, remain - remain_count + 1)
            lower_bound = max(1, remain - 5*(remain_count-1))
            res = np.random.randint(lower_bound, upper_bound+1)
            remain = remain - res
            result.append(res)
        
        result =  np.array(result)
        np.random.shuffle(result)
        return tuple(result)

    def data_init(self) -> None:
        self.task_data[10][0] = np.array([(30, 14), (45, 12), (60, 7), (90, 6), (180, 16)], dtype=self.tasktype)
        self.task_data[10][1] = np.array([(30, 5), (36, 13), (60, 19), (90, 8), (180, 12)], dtype=self.tasktype)
        self.task_data[10][2] = np.array([(20, 6), (45, 17), (60, 11), (90, 8), (180, 9)], dtype=self.tasktype)
        self.task_data[10][3] = np.array([(30, 13), (36, 8), (60, 7), (90, 17), (180, 7)], dtype=self.tasktype)
        self.task_data[10][4] = np.array([(36, 11), (45, 14), (60, 11), (90, 10), (180, 17)], dtype=self.tasktype)
        self.task_data[10][5] = np.array([(20, 7), (36, 6), (45, 13), (90, 8), (180, 19)], dtype=self.tasktype)
        self.task_data[10][6] = np.array([(30, 6), (45, 16), (60, 11), (90, 13), (180, 21)], dtype=self.tasktype)
        self.task_data[10][7] = np.array([(18, 6), (36, 15), (45, 6), (90, 8), (180, 5)], dtype=self.tasktype)
        self.task_data[10][8] = np.array([(18, 8), (45, 13), (60, 7), (90, 8), (180, 12)], dtype=self.tasktype)
        self.task_data[10][9] = np.array([(18, 6), (36, 8), (45, 8), (60, 14), (180, 7)], dtype=self.tasktype)
        self.task_data[10][10] = np.array([(20, 9), (36, 6), (45, 12), (90, 8), (180, 5)], dtype=self.tasktype)
        self.task_data[10][11] = np.array([(30, 6), (45, 13), (60, 11), (90, 18), (180, 23)], dtype=self.tasktype)
        self.task_data[10][12] = np.array([(12, 7), (45, 6), (60, 10), (90, 5), (180, 10)], dtype=self.tasktype)
        self.task_data[10][13] = np.array([(30, 11), (36, 7), (45, 11), (90, 13), (180, 9)], dtype=self.tasktype)
        self.task_data[10][14] = np.array([(36, 10), (45, 10), (60, 11), (90, 24), (180, 10)], dtype=self.tasktype)
        self.task_data[10][15] = np.array([(20, 6), (45, 17), (60, 10), (90, 11), (180, 6)], dtype=self.tasktype)
        self.task_data[10][16] = np.array([(18, 7), (36, 7), (45, 7), (60, 9), (180, 20)], dtype=self.tasktype)
        self.task_data[10][17] = np.array([(30, 6), (36, 8), (60, 19), (90, 15), (180, 17)], dtype=self.tasktype)
        self.task_data[10][18] = np.array([(20, 5), (30, 11), (45, 5), (90, 19), (180, 10)], dtype=self.tasktype)
        self.task_data[10][19] = np.array([(20, 6), (30, 5), (60, 14), (90, 22), (180, 9)], dtype=self.tasktype)
        self.task_data[11][0] = np.array([(30, 11), (45, 14), (60, 7), (90, 19), (180, 18)], dtype=self.tasktype)
        self.task_data[11][1] = np.array([(36, 10), (45, 16), (60, 18), (90, 6), (180, 19)], dtype=self.tasktype)
        self.task_data[11][2] = np.array([(30, 7), (36, 17), (60, 7), (90, 14), (180, 23)], dtype=self.tasktype)
        self.task_data[11][3] = np.array([(30, 6), (36, 14), (60, 23), (90, 7), (180, 9)], dtype=self.tasktype)
        self.task_data[11][4] = np.array([(20, 9), (30, 7), (60, 7), (90, 15), (180, 25)], dtype=self.tasktype)
        self.task_data[11][5] = np.array([(20, 6), (36, 11), (45, 13), (90, 11), (180, 14)], dtype=self.tasktype)
        self.task_data[11][6] = np.array([(18, 8), (45, 8), (60, 13), (90, 18), (180, 11)], dtype=self.tasktype)
        self.task_data[11][7] = np.array([(30, 9), (36, 16), (60, 14), (90, 8), (180, 5)], dtype=self.tasktype)
        self.task_data[11][8] = np.array([(36, 7), (45, 24), (60, 6), (90, 13), (180, 22)], dtype=self.tasktype)
        self.task_data[11][9] = np.array([(18, 11), (36, 7), (45, 8), (90, 6), (180, 9)], dtype=self.tasktype)
        self.task_data[11][10] = np.array([(20, 5), (45, 23), (60, 8), (90, 7), (180, 23)], dtype=self.tasktype)
        self.task_data[11][11] = np.array([(20, 7), (36, 5), (45, 13), (90, 19), (180, 19)], dtype=self.tasktype)
        self.task_data[11][12] = np.array([(36, 5), (45, 16), (60, 22), (90, 17), (180, 8)], dtype=self.tasktype)
        self.task_data[11][13] = np.array([(18, 5), (45, 14), (60, 13), (90, 16), (180, 20)], dtype=self.tasktype)
        self.task_data[11][14] = np.array([(36, 14), (45, 19), (60, 5), (90, 7), (180, 22)], dtype=self.tasktype)
        self.task_data[11][15] = np.array([(36, 13), (45, 9), (60, 21), (90, 14), (180, 8)], dtype=self.tasktype)
        self.task_data[11][16] = np.array([(20, 7), (30, 9), (60, 14), (90, 9), (180, 20)], dtype=self.tasktype)
        self.task_data[11][17] = np.array([(18, 7), (45, 9), (60, 12), (90, 19), (180, 17)], dtype=self.tasktype)
        self.task_data[11][18] = np.array([(30, 7), (45, 14), (60, 15), (90, 19), (180, 18)], dtype=self.tasktype)
        self.task_data[11][19] = np.array([(18, 6), (30, 13), (36, 7), (60, 7), (180, 5)], dtype=self.tasktype)
        self.task_data[12][0] = np.array([(12, 7), (36, 13), (60, 9), (90, 6), (180, 5)], dtype=self.tasktype)
        self.task_data[12][1] = np.array([(20, 8), (36, 15), (60, 5), (90, 20), (180, 14)], dtype=self.tasktype)
        self.task_data[12][2] = np.array([(30, 6), (36, 11), (45, 9), (60, 23), (180, 19)], dtype=self.tasktype)
        self.task_data[12][3] = np.array([(18, 5), (36, 22), (45, 7), (60, 6), (180, 9)], dtype=self.tasktype)
        self.task_data[12][4] = np.array([(30, 13), (45, 13), (60, 11), (90, 23), (180, 7)], dtype=self.tasktype)
        self.task_data[12][5] = np.array([(30, 8), (36, 13), (45, 18), (60, 6), (180, 14)], dtype=self.tasktype)
        self.task_data[12][6] = np.array([(36, 11), (45, 13), (60, 23), (90, 17), (180, 5)], dtype=self.tasktype)
        self.task_data[12][7] = np.array([(18, 10), (36, 9), (45, 12), (90, 7), (180, 9)], dtype=self.tasktype)
        self.task_data[12][8] = np.array([(30, 11), (45, 15), (60, 19), (90, 11), (180, 12)], dtype=self.tasktype)
        self.task_data[12][9] = np.array([(15, 6), (36, 9), (60, 22), (90, 5), (180, 21)], dtype=self.tasktype)
        self.task_data[12][10] = np.array([(30, 17), (36, 11), (60, 8), (90, 13), (180, 8)], dtype=self.tasktype)
        self.task_data[12][11] = np.array([(30, 8), (36, 7), (45, 24), (90, 7), (180, 22)], dtype=self.tasktype)
        self.task_data[12][12] = np.array([(9, 5), (30, 8), (60, 9), (90, 11), (180, 19)], dtype=self.tasktype)
        self.task_data[12][13] = np.array([(15, 7), (36, 6), (45, 11), (90, 23), (180, 13)], dtype=self.tasktype)
        self.task_data[12][14] = np.array([(12, 5), (30, 9), (45, 11), (60, 13), (180, 5)], dtype=self.tasktype)
        self.task_data[12][15] = np.array([(20, 11), (30, 6), (36, 9), (90, 10), (180, 17)], dtype=self.tasktype)
        self.task_data[12][16] = np.array([(20, 9), (36, 10), (60, 17), (90, 5), (180, 24)], dtype=self.tasktype)
        self.task_data[12][17] = np.array([(36, 10), (45, 19), (60, 14), (90, 17), (180, 15)], dtype=self.tasktype)
        self.task_data[12][18] = np.array([(36, 19), (45, 12), (60, 5), (90, 23), (180, 11)], dtype=self.tasktype)
        self.task_data[12][19] = np.array([(15, 7), (45, 8), (60, 17), (90, 19), (180, 10)], dtype=self.tasktype)
        self.task_data[13][0] = np.array([(20, 9), (36, 16), (60, 9), (90, 10), (180, 24)], dtype=self.tasktype)
        self.task_data[13][1] = np.array([(20, 8), (45, 14), (60, 18), (90, 17), (180, 19)], dtype=self.tasktype)
        self.task_data[13][2] = np.array([(20, 7), (36, 9), (60, 23), (90, 16), (180, 25)], dtype=self.tasktype)
        self.task_data[13][3] = np.array([(15, 7), (36, 12), (60, 13), (90, 17), (180, 17)], dtype=self.tasktype)
        self.task_data[13][4] = np.array([(20, 5), (30, 19), (60, 11), (90, 16), (180, 10)], dtype=self.tasktype)
        self.task_data[13][5] = np.array([(20, 17), (45, 6), (60, 8), (90, 9), (180, 15)], dtype=self.tasktype)
        self.task_data[13][6] = np.array([(30, 15), (45, 13), (60, 11), (90, 25), (180, 9)], dtype=self.tasktype)
        self.task_data[13][7] = np.array([(18, 8), (36, 17), (60, 5), (90, 20), (180, 13)], dtype=self.tasktype)
        self.task_data[13][8] = np.array([(20, 8), (30, 11), (36, 7), (90, 25), (180, 11)], dtype=self.tasktype)
        self.task_data[13][9] = np.array([(20, 14), (36, 6), (45, 7), (90, 14), (180, 22)], dtype=self.tasktype)
        self.task_data[13][10] = np.array([(36, 13), (45, 19), (60, 21), (90, 10), (180, 9)], dtype=self.tasktype)
        self.task_data[13][11] = np.array([(30, 13), (36, 10), (45, 14), (90, 21), (180, 8)], dtype=self.tasktype)
        self.task_data[13][12] = np.array([(20, 11), (36, 9), (45, 13), (60, 11), (180, 5)], dtype=self.tasktype)
        self.task_data[13][13] = np.array([(30, 7), (45, 19), (60, 21), (90, 17), (180, 20)], dtype=self.tasktype)
        self.task_data[13][14] = np.array([(12, 5), (20, 7), (36, 11), (90, 11), (180, 19)], dtype=self.tasktype)
        self.task_data[13][15] = np.array([(15, 8), (18, 6), (36, 5), (60, 11), (180, 19)], dtype=self.tasktype)
        self.task_data[13][16] = np.array([(30, 16), (45, 8), (60, 19), (90, 22), (180, 6)], dtype=self.tasktype)
        self.task_data[13][17] = np.array([(30, 9), (36, 16), (60, 13), (90, 21), (180, 19)], dtype=self.tasktype)
        self.task_data[13][18] = np.array([(18, 9), (30, 13), (60, 8), (90, 14), (180, 14)], dtype=self.tasktype)
        self.task_data[13][19] = np.array([(30, 12), (45, 14), (60, 19), (90, 18), (180, 13)], dtype=self.tasktype)
        self.task_data[14][0] = np.array([(30, 18), (36, 9), (60, 17), (90, 17), (180, 14)], dtype=self.tasktype)
        self.task_data[14][1] = np.array([(20, 7), (30, 17), (45, 17), (90, 6), (180, 7)], dtype=self.tasktype)
        self.task_data[14][2] = np.array([(30, 9), (36, 19), (60, 10), (90, 24), (180, 25)], dtype=self.tasktype)
        self.task_data[14][3] = np.array([(30, 13), (36, 16), (60, 14), (90, 15), (180, 21)], dtype=self.tasktype)
        self.task_data[14][4] = np.array([(30, 18), (36, 14), (45, 7), (60, 11), (180, 13)], dtype=self.tasktype)
        self.task_data[14][5] = np.array([(18, 10), (36, 17), (45, 9), (90, 8), (180, 17)], dtype=self.tasktype)
        self.task_data[14][6] = np.array([(20, 8), (45, 13), (60, 21), (90, 21), (180, 23)], dtype=self.tasktype)
        self.task_data[14][7] = np.array([(36, 16), (45, 22), (60, 9), (90, 21), (180, 16)], dtype=self.tasktype)
        self.task_data[14][8] = np.array([(15, 10), (36, 8), (60, 17), (90, 12), (180, 17)], dtype=self.tasktype)
        self.task_data[14][9] = np.array([(12, 10), (45, 7), (60, 18), (90, 7), (180, 6)], dtype=self.tasktype)
        self.task_data[14][10] = np.array([(36, 8), (45, 23), (60, 22), (90, 20), (180, 13)], dtype=self.tasktype)
        self.task_data[14][11] = np.array([(30, 23), (45, 15), (60, 7), (90, 10), (180, 13)], dtype=self.tasktype)
        self.task_data[14][12] = np.array([(12, 8), (30, 9), (45, 7), (90, 19), (180, 13)], dtype=self.tasktype)
        self.task_data[14][13] = np.array([(18, 13), (36, 7), (45, 14), (90, 9), (180, 12)], dtype=self.tasktype)
        self.task_data[14][14] = np.array([(10, 8), (30, 6), (60, 13), (90, 7), (180, 20)], dtype=self.tasktype)
        self.task_data[14][15] = np.array([(20, 11), (30, 13), (60, 12), (90, 14), (180, 10)], dtype=self.tasktype)
        self.task_data[14][16] = np.array([(18, 16), (30, 6), (45, 6), (60, 9), (180, 5)], dtype=self.tasktype)
        self.task_data[14][17] = np.array([(18, 11), (36, 10), (45, 7), (60, 17), (180, 13)], dtype=self.tasktype)
        self.task_data[14][18] = np.array([(20, 12), (45, 8), (60, 18), (90, 20), (180, 19)], dtype=self.tasktype)
        self.task_data[14][19] = np.array([(36, 17), (45, 19), (60, 16), (90, 13), (180, 17)], dtype=self.tasktype)
        self.task_data[15][0] = np.array([(20, 19), (36, 6), (45, 9), (90, 6), (180, 21)], dtype=self.tasktype)
        self.task_data[15][1] = np.array([(30, 7), (36, 23), (45, 19), (90, 8), (180, 21)], dtype=self.tasktype)
        self.task_data[15][2] = np.array([(10, 6), (20, 10), (45, 7), (90, 17), (180, 11)], dtype=self.tasktype)
        self.task_data[15][3] = np.array([(12, 11), (45, 7), (60, 11), (90, 17), (180, 9)], dtype=self.tasktype)
        self.task_data[15][4] = np.array([(12, 7), (18, 5), (45, 16), (60, 9), (180, 24)], dtype=self.tasktype)
        self.task_data[15][5] = np.array([(18, 14), (36, 7), (45, 19), (90, 6), (180, 6)], dtype=self.tasktype)
        self.task_data[15][6] = np.array([(18, 7), (30, 19), (36, 5), (60, 17), (180, 10)], dtype=self.tasktype)
        self.task_data[15][7] = np.array([(10, 6), (18, 7), (60, 9), (90, 23), (180, 19)], dtype=self.tasktype)
        self.task_data[15][8] = np.array([(30, 22), (36, 11), (45, 11), (90, 14), (180, 11)], dtype=self.tasktype)
        self.task_data[15][9] = np.array([(20, 9), (45, 23), (60, 9), (90, 25), (180, 20)], dtype=self.tasktype)
        self.task_data[15][10] = np.array([(18, 10), (20, 11), (45, 8), (90, 17), (180, 5)], dtype=self.tasktype)
        self.task_data[15][11] = np.array([(18, 7), (30, 7), (36, 21), (90, 19), (180, 14)], dtype=self.tasktype)
        self.task_data[15][12] = np.array([(20, 13), (36, 11), (60, 22), (90, 13), (180, 5)], dtype=self.tasktype)
        self.task_data[15][13] = np.array([(20, 15), (45, 13), (60, 20), (90, 8), (180, 7)], dtype=self.tasktype)
        self.task_data[15][14] = np.array([(10, 10), (36, 5), (60, 9), (90, 14), (180, 11)], dtype=self.tasktype)
        self.task_data[15][15] = np.array([(30, 14), (36, 22), (45, 8), (90, 9), (180, 25)], dtype=self.tasktype)
        self.task_data[15][16] = np.array([(20, 9), (36, 12), (45, 14), (60, 21), (180, 9)], dtype=self.tasktype)
        self.task_data[15][17] = np.array([(18, 15), (36, 7), (45, 9), (60, 14), (180, 7)], dtype=self.tasktype)
        self.task_data[15][18] = np.array([(15, 7), (36, 19), (45, 10), (60, 15), (180, 6)], dtype=self.tasktype)
        self.task_data[15][19] = np.array([(12, 10), (36, 9), (45, 7), (60, 13), (180, 9)], dtype=self.tasktype)
        self.task_data[16][0] = np.array([(18, 9), (36, 17), (45, 23), (90, 6), (180, 9)], dtype=self.tasktype)
        self.task_data[16][1] = np.array([(10, 5), (18, 10), (60, 23), (90, 6), (180, 16)], dtype=self.tasktype)
        self.task_data[16][2] = np.array([(12, 5), (30, 19), (45, 11), (60, 13), (180, 17)], dtype=self.tasktype)
        self.task_data[16][3] = np.array([(18, 7), (20, 13), (60, 15), (90, 20), (180, 15)], dtype=self.tasktype)
        self.task_data[16][4] = np.array([(30, 23), (45, 12), (60, 18), (90, 13), (180, 22)], dtype=self.tasktype)
        self.task_data[16][5] = np.array([(30, 19), (36, 25), (60, 6), (90, 10), (180, 11)], dtype=self.tasktype)
        self.task_data[16][6] = np.array([(20, 6), (30, 12), (36, 25), (60, 8), (180, 15)], dtype=self.tasktype)
        self.task_data[16][7] = np.array([(36, 19), (45, 23), (60, 21), (90, 16), (180, 6)], dtype=self.tasktype)
        self.task_data[16][8] = np.array([(9, 8), (36, 5), (45, 14), (60, 12), (180, 11)], dtype=self.tasktype)
        self.task_data[16][9] = np.array([(15, 7), (36, 17), (45, 11), (60, 22), (180, 8)], dtype=self.tasktype)
        self.task_data[16][10] = np.array([(15, 7), (20, 14), (36, 9), (90, 9), (180, 15)], dtype=self.tasktype)
        self.task_data[16][11] = np.array([(30, 13), (36, 11), (45, 24), (90, 23), (180, 12)], dtype=self.tasktype)
        self.task_data[16][12] = np.array([(20, 11), (36, 23), (60, 16), (90, 8), (180, 11)], dtype=self.tasktype)
        self.task_data[16][13] = np.array([(15, 12), (36, 15), (60, 13), (90, 11), (180, 8)], dtype=self.tasktype)
        self.task_data[16][14] = np.array([(12, 6), (18, 11), (45, 17), (90, 7), (180, 7)], dtype=self.tasktype)
        self.task_data[16][15] = np.array([(36, 15), (45, 23), (60, 19), (90, 20), (180, 23)], dtype=self.tasktype)
        self.task_data[16][16] = np.array([(20, 17), (30, 8), (45, 14), (90, 7), (180, 17)], dtype=self.tasktype)
        self.task_data[16][17] = np.array([(20, 11), (36, 17), (45, 9), (60, 19), (180, 10)], dtype=self.tasktype)
        self.task_data[16][18] = np.array([(18, 11), (20, 11), (36, 11), (90, 9), (180, 7)], dtype=self.tasktype)
        self.task_data[16][19] = np.array([(20, 9), (30, 17), (60, 17), (90, 18), (180, 17)], dtype=self.tasktype)
        self.task_data[17][0] = np.array([(10, 6), (20, 7), (30, 14), (90, 13), (180, 25)], dtype=self.tasktype)
        self.task_data[17][1] = np.array([(20, 8), (30, 17), (45, 17), (60, 17), (180, 13)], dtype=self.tasktype)
        self.task_data[17][2] = np.array([(18, 8), (20, 11), (60, 22), (90, 20), (180, 23)], dtype=self.tasktype)
        self.task_data[17][3] = np.array([(20, 7), (36, 22), (45, 22), (90, 18), (180, 9)], dtype=self.tasktype)
        self.task_data[17][4] = np.array([(18, 13), (36, 21), (45, 8), (60, 10), (180, 8)], dtype=self.tasktype)
        self.task_data[17][5] = np.array([(20, 17), (36, 5), (45, 14), (60, 18), (180, 18)], dtype=self.tasktype)
        self.task_data[17][6] = np.array([(15, 12), (45, 22), (60, 14), (90, 10), (180, 12)], dtype=self.tasktype)
        self.task_data[17][7] = np.array([(9, 6), (20, 11), (60, 11), (90, 23), (180, 9)], dtype=self.tasktype)
        self.task_data[17][8] = np.array([(30, 23), (45, 16), (60, 17), (90, 19), (180, 14)], dtype=self.tasktype)
        self.task_data[17][9] = np.array([(18, 13), (30, 17), (36, 5), (90, 21), (180, 7)], dtype=self.tasktype)
        self.task_data[17][10] = np.array([(20, 19), (36, 12), (45, 12), (90, 5), (180, 16)], dtype=self.tasktype)
        self.task_data[17][11] = np.array([(18, 15), (45, 22), (60, 6), (90, 13), (180, 25)], dtype=self.tasktype)
        self.task_data[17][12] = np.array([(12, 7), (20, 6), (30, 13), (45, 14), (180, 14)], dtype=self.tasktype)
        self.task_data[17][13] = np.array([(20, 15), (30, 13), (60, 17), (90, 18), (180, 7)], dtype=self.tasktype)
        self.task_data[17][14] = np.array([(15, 6), (20, 19), (60, 9), (90, 15), (180, 6)], dtype=self.tasktype)
        self.task_data[17][15] = np.array([(15, 13), (45, 14), (60, 16), (90, 20), (180, 6)], dtype=self.tasktype)
        self.task_data[17][16] = np.array([(30, 16), (36, 15), (45, 23), (90, 17), (180, 8)], dtype=self.tasktype)
        self.task_data[17][17] = np.array([(15, 11), (36, 13), (60, 21), (90, 14), (180, 19)], dtype=self.tasktype)
        self.task_data[17][18] = np.array([(20, 5), (30, 23), (60, 17), (90, 24), (180, 25)], dtype=self.tasktype)
        self.task_data[17][19] = np.array([(30, 23), (36, 7), (45, 14), (60, 22), (180, 11)], dtype=self.tasktype)
        self.task_data[18][0] = np.array([(18, 16), (30, 12), (36, 10), (90, 17), (180, 9)], dtype=self.tasktype)
        self.task_data[18][1] = np.array([(10, 7), (20, 6), (30, 18), (90, 8), (180, 20)], dtype=self.tasktype)
        self.task_data[18][2] = np.array([(18, 11), (36, 23), (45, 16), (60, 9), (180, 8)], dtype=self.tasktype)
        self.task_data[18][3] = np.array([(20, 15), (30, 23), (45, 7), (60, 6), (180, 5)], dtype=self.tasktype)
        self.task_data[18][4] = np.array([(20, 20), (30, 9), (60, 6), (90, 25), (180, 23)], dtype=self.tasktype)
        self.task_data[18][5] = np.array([(18, 16), (36, 16), (60, 11), (90, 23), (180, 5)], dtype=self.tasktype)
        self.task_data[18][6] = np.array([(12, 9), (30, 11), (45, 20), (90, 18), (180, 7)], dtype=self.tasktype)
        self.task_data[18][7] = np.array([(15, 13), (18, 10), (36, 6), (90, 13), (180, 14)], dtype=self.tasktype)
        self.task_data[18][8] = np.array([(18, 12), (20, 11), (36, 14), (60, 7), (180, 15)], dtype=self.tasktype)
        self.task_data[18][9] = np.array([(12, 10), (36, 10), (45, 23), (90, 13), (180, 7)], dtype=self.tasktype)
        self.task_data[18][10] = np.array([(12, 5), (18, 15), (36, 10), (60, 13), (180, 8)], dtype=self.tasktype)
        self.task_data[18][11] = np.array([(12, 9), (20, 11), (60, 12), (90, 17), (180, 20)], dtype=self.tasktype)
        self.task_data[18][12] = np.array([(15, 13), (18, 7), (36, 8), (60, 17), (180, 6)], dtype=self.tasktype)
        self.task_data[18][13] = np.array([(18, 13), (36, 19), (45, 12), (90, 18), (180, 15)], dtype=self.tasktype)
        self.task_data[18][14] = np.array([(20, 15), (30, 19), (36, 7), (90, 14), (180, 12)], dtype=self.tasktype)
        self.task_data[18][15] = np.array([(18, 13), (30, 23), (60, 11), (90, 6), (180, 11)], dtype=self.tasktype)
        self.task_data[18][16] = np.array([(18, 13), (30, 13), (45, 19), (60, 9), (180, 13)], dtype=self.tasktype)
        self.task_data[18][17] = np.array([(18, 9), (20, 15), (45, 21), (90, 5), (180, 5)], dtype=self.tasktype)
        self.task_data[18][18] = np.array([(18, 10), (36, 15), (45, 23), (90, 24), (180, 9)], dtype=self.tasktype)
        self.task_data[18][19] = np.array([(20, 9), (30, 18), (45, 21), (90, 19), (180, 13)], dtype=self.tasktype)
        self.task_data[19][0] = np.array([(18, 15), (20, 5), (36, 23), (90, 11), (180, 9)], dtype=self.tasktype)
        self.task_data[19][1] = np.array([(12, 11), (30, 6), (36, 15), (45, 13), (180, 15)], dtype=self.tasktype)
        self.task_data[19][2] = np.array([(10, 9), (30, 7), (36, 23), (90, 5), (180, 13)], dtype=self.tasktype)
        self.task_data[19][3] = np.array([(10, 7), (12, 7), (36, 11), (90, 24), (180, 8)], dtype=self.tasktype)
        self.task_data[19][4] = np.array([(15, 8), (20, 17), (45, 7), (60, 17), (180, 13)], dtype=self.tasktype)
        self.task_data[19][5] = np.array([(18, 14), (36, 23), (45, 16), (90, 6), (180, 9)], dtype=self.tasktype)
        self.task_data[19][6] = np.array([(12, 9), (20, 7), (36, 25), (90, 7), (180, 6)], dtype=self.tasktype)
        self.task_data[19][7] = np.array([(20, 14), (36, 22), (60, 25), (90, 12), (180, 7)], dtype=self.tasktype)
        self.task_data[19][8] = np.array([(10, 6), (20, 13), (30, 6), (45, 14), (180, 25)], dtype=self.tasktype)
        self.task_data[19][9] = np.array([(6, 5), (36, 25), (45, 6), (90, 19), (180, 6)], dtype=self.tasktype)
        self.task_data[19][10] = np.array([(20, 7), (30, 22), (36, 22), (90, 13), (180, 11)], dtype=self.tasktype)
        self.task_data[19][11] = np.array([(12, 7), (18, 5), (36, 23), (45, 16), (180, 6)], dtype=self.tasktype)
        self.task_data[19][12] = np.array([(15, 14), (30, 12), (36, 5), (60, 19), (180, 19)], dtype=self.tasktype)
        self.task_data[19][13] = np.array([(12, 11), (30, 11), (45, 19), (90, 11), (180, 12)], dtype=self.tasktype)
        self.task_data[19][14] = np.array([(15, 7), (20, 14), (45, 25), (90, 6), (180, 19)], dtype=self.tasktype)
        self.task_data[19][15] = np.array([(12, 9), (30, 11), (36, 19), (45, 6), (180, 23)], dtype=self.tasktype)
        self.task_data[19][16] = np.array([(12, 10), (20, 11), (60, 11), (90, 24), (180, 11)], dtype=self.tasktype)
        self.task_data[19][17] = np.array([(9, 7), (15, 9), (45, 10), (90, 24), (180, 6)], dtype=self.tasktype)
        self.task_data[19][18] = np.array([(18, 11), (30, 23), (60, 15), (90, 21), (180, 7)], dtype=self.tasktype)
        self.task_data[19][19] = np.array([(10, 5), (30, 18), (45, 22), (90, 23), (180, 9)], dtype=self.tasktype)
        self.task_data[20][0] = np.array([(20, 13), (36, 20), (45, 22), (90, 16), (180, 23)], dtype=self.tasktype)
        self.task_data[20][1] = np.array([(10, 8), (20, 17), (45, 10), (90, 8), (180, 7)], dtype=self.tasktype)
        self.task_data[20][2] = np.array([(15, 8), (20, 16), (30, 9), (45, 11), (180, 23)], dtype=self.tasktype)
        self.task_data[20][3] = np.array([(15, 14), (18, 8), (20, 7), (90, 20), (180, 8)], dtype=self.tasktype)
        self.task_data[20][4] = np.array([(15, 6), (18, 16), (45, 12), (60, 19), (180, 23)], dtype=self.tasktype)
        self.task_data[20][5] = np.array([(12, 12), (15, 9), (60, 8), (90, 17), (180, 14)], dtype=self.tasktype)
        self.task_data[20][6] = np.array([(12, 5), (20, 15), (45, 22), (60, 19), (180, 5)], dtype=self.tasktype)
        self.task_data[20][7] = np.array([(20, 13), (30, 13), (36, 19), (45, 14), (180, 15)], dtype=self.tasktype)
        self.task_data[20][8] = np.array([(20, 17), (30, 17), (45, 9), (90, 23), (180, 22)], dtype=self.tasktype)
        self.task_data[20][9] = np.array([(9, 7), (18, 13), (60, 12), (90, 23), (180, 7)], dtype=self.tasktype)
        self.task_data[20][10] = np.array([(18, 14), (20, 10), (30, 14), (90, 16), (180, 14)], dtype=self.tasktype)
        self.task_data[20][11] = np.array([(9, 7), (20, 6), (30, 18), (60, 15), (180, 13)], dtype=self.tasktype)
        self.task_data[20][12] = np.array([(9, 8), (18, 7), (45, 24), (90, 14), (180, 5)], dtype=self.tasktype)
        self.task_data[20][13] = np.array([(18, 6), (20, 19), (36, 16), (45, 6), (180, 25)], dtype=self.tasktype)
        self.task_data[20][14] = np.array([(15, 9), (20, 10), (30, 15), (36, 13), (180, 7)], dtype=self.tasktype)
        self.task_data[20][15] = np.array([(20, 16), (30, 17), (36, 16), (90, 11), (180, 11)], dtype=self.tasktype)
        self.task_data[20][16] = np.array([(12, 11), (20, 11), (45, 13), (90, 19), (180, 5)], dtype=self.tasktype)
        self.task_data[20][17] = np.array([(18, 5), (20, 17), (36, 19), (45, 12), (180, 15)], dtype=self.tasktype)
        self.task_data[20][18] = np.array([(15, 6), (30, 23), (36, 21), (60, 11), (180, 11)], dtype=self.tasktype)
        self.task_data[20][19] = np.array([(20, 11), (30, 25), (36, 13), (90, 20), (180, 6)], dtype=self.tasktype)
        self.task_data[21][0] = np.array([(15, 9), (30, 13), (36, 22), (45, 19), (180, 6)], dtype=self.tasktype)
        self.task_data[21][1] = np.array([(9, 7), (20, 17), (30, 11), (90, 5), (180, 9)], dtype=self.tasktype)
        self.task_data[21][2] = np.array([(18, 6), (20, 12), (36, 23), (45, 22), (180, 6)], dtype=self.tasktype)
        self.task_data[21][3] = np.array([(20, 18), (36, 20), (60, 21), (90, 23), (180, 6)], dtype=self.tasktype)
        self.task_data[21][4] = np.array([(20, 19), (30, 7), (36, 25), (90, 17), (180, 6)], dtype=self.tasktype)
        self.task_data[21][5] = np.array([(15, 13), (20, 10), (45, 22), (90, 19), (180, 7)], dtype=self.tasktype)
        self.task_data[21][6] = np.array([(12, 10), (20, 12), (45, 23), (90, 11), (180, 6)], dtype=self.tasktype)
        self.task_data[21][7] = np.array([(9, 7), (36, 11), (45, 25), (60, 22), (180, 17)], dtype=self.tasktype)
        self.task_data[21][8] = np.array([(10, 9), (30, 23), (60, 9), (90, 21), (180, 9)], dtype=self.tasktype)
        self.task_data[21][9] = np.array([(18, 17), (30, 11), (36, 17), (45, 12), (180, 8)], dtype=self.tasktype)
        self.task_data[21][10] = np.array([(18, 13), (36, 21), (45, 13), (60, 24), (180, 19)], dtype=self.tasktype)
        self.task_data[21][11] = np.array([(12, 10), (20, 10), (36, 6), (45, 22), (180, 21)], dtype=self.tasktype)
        self.task_data[21][12] = np.array([(12, 11), (30, 8), (45, 20), (60, 21), (180, 21)], dtype=self.tasktype)
        self.task_data[21][13] = np.array([(9, 8), (18, 6), (36, 19), (60, 18), (180, 10)], dtype=self.tasktype)
        self.task_data[21][14] = np.array([(20, 17), (30, 16), (36, 18), (60, 9), (180, 12)], dtype=self.tasktype)
        self.task_data[21][15] = np.array([(12, 9), (20, 13), (45, 14), (60, 18), (180, 17)], dtype=self.tasktype)
        self.task_data[21][16] = np.array([(12, 11), (20, 11), (36, 10), (90, 23), (180, 18)], dtype=self.tasktype)
        self.task_data[21][17] = np.array([(6, 5), (15, 8), (30, 18), (90, 8), (180, 7)], dtype=self.tasktype)
        self.task_data[21][18] = np.array([(15, 13), (30, 18), (36, 17), (90, 10), (180, 10)], dtype=self.tasktype)
        self.task_data[21][19] = np.array([(12, 10), (36, 25), (60, 17), (90, 21), (180, 9)], dtype=self.tasktype)
        self.task_data[22][0] = np.array([(12, 7), (20, 19), (30, 13), (45, 8), (180, 9)], dtype=self.tasktype)
        self.task_data[22][1] = np.array([(15, 13), (30, 13), (36, 17), (45, 17), (180, 10)], dtype=self.tasktype)
        self.task_data[22][2] = np.array([(18, 17), (20, 11), (36, 7), (60, 23), (180, 24)], dtype=self.tasktype)
        self.task_data[22][3] = np.array([(10, 5), (12, 6), (30, 19), (36, 17), (180, 17)], dtype=self.tasktype)
        self.task_data[22][4] = np.array([(12, 11), (15, 8), (20, 8), (45, 13), (180, 10)], dtype=self.tasktype)
        self.task_data[22][5] = np.array([(10, 5), (18, 13), (20, 13), (60, 14), (180, 19)], dtype=self.tasktype)
        self.task_data[22][6] = np.array([(18, 9), (20, 18), (30, 14), (36, 10), (180, 11)], dtype=self.tasktype)
        self.task_data[22][7] = np.array([(9, 8), (18, 11), (36, 21), (90, 7), (180, 8)], dtype=self.tasktype)
        self.task_data[22][8] = np.array([(15, 13), (18, 13), (60, 16), (90, 21), (180, 20)], dtype=self.tasktype)
        self.task_data[22][9] = np.array([(15, 14), (18, 6), (36, 17), (45, 15), (180, 23)], dtype=self.tasktype)
        self.task_data[22][10] = np.array([(12, 5), (15, 14), (30, 17), (36, 6), (180, 20)], dtype=self.tasktype)
        self.task_data[22][11] = np.array([(10, 7), (30, 21), (36, 13), (45, 17), (180, 11)], dtype=self.tasktype)
        self.task_data[22][12] = np.array([(10, 7), (15, 13), (45, 17), (90, 20), (180, 5)], dtype=self.tasktype)
        self.task_data[22][13] = np.array([(9, 8), (10, 9), (60, 12), (90, 13), (180, 11)], dtype=self.tasktype)
        self.task_data[22][14] = np.array([(15, 12), (18, 13), (20, 9), (60, 7), (180, 20)], dtype=self.tasktype)
        self.task_data[22][15] = np.array([(12, 11), (15, 8), (20, 10), (36, 7), (180, 9)], dtype=self.tasktype)
        self.task_data[22][16] = np.array([(12, 11), (15, 6), (36, 23), (45, 9), (180, 8)], dtype=self.tasktype)
        self.task_data[22][17] = np.array([(12, 11), (18, 14), (36, 11), (60, 9), (180, 9)], dtype=self.tasktype)
        self.task_data[22][18] = np.array([(12, 9), (15, 12), (36, 13), (60, 12), (180, 15)], dtype=self.tasktype)
        self.task_data[22][19] = np.array([(15, 7), (18, 13), (36, 25), (45, 9), (180, 20)], dtype=self.tasktype)
        self.task_data[23][0] = np.array([(20, 17), (30, 17), (36, 22), (60, 12), (180, 13)], dtype=self.tasktype)
        self.task_data[23][1] = np.array([(12, 12), (30, 13), (36, 19), (90, 23), (180, 15)], dtype=self.tasktype)
        self.task_data[23][2] = np.array([(15, 14), (18, 13), (20, 6), (45, 11), (180, 19)], dtype=self.tasktype)
        self.task_data[23][3] = np.array([(18, 10), (20, 11), (30, 18), (36, 19), (180, 12)], dtype=self.tasktype)
        self.task_data[23][4] = np.array([(15, 10), (20, 17), (30, 11), (45, 14), (180, 19)], dtype=self.tasktype)
        self.task_data[23][5] = np.array([(18, 17), (20, 11), (45, 24), (90, 22), (180, 5)], dtype=self.tasktype)
        self.task_data[23][6] = np.array([(12, 11), (18, 9), (36, 21), (45, 11), (180, 11)], dtype=self.tasktype)
        self.task_data[23][7] = np.array([(18, 13), (30, 17), (36, 14), (45, 23), (180, 19)], dtype=self.tasktype)
        self.task_data[23][8] = np.array([(9, 8), (10, 9), (60, 19), (90, 14), (180, 7)], dtype=self.tasktype)
        self.task_data[23][9] = np.array([(15, 12), (20, 19), (36, 5), (45, 16), (180, 9)], dtype=self.tasktype)
        self.task_data[23][10] = np.array([(12, 11), (18, 6), (20, 17), (45, 7), (180, 8)], dtype=self.tasktype)
        self.task_data[23][11] = np.array([(15, 14), (18, 16), (60, 18), (90, 9), (180, 15)], dtype=self.tasktype)
        self.task_data[23][12] = np.array([(30, 24), (36, 22), (45, 25), (90, 22), (180, 15)], dtype=self.tasktype)
        self.task_data[23][13] = np.array([(20, 17), (30, 17), (36, 19), (60, 16), (180, 16)], dtype=self.tasktype)
        self.task_data[23][14] = np.array([(12, 11), (30, 12), (36, 19), (45, 19), (180, 6)], dtype=self.tasktype)
        self.task_data[23][15] = np.array([(15, 13), (18, 7), (20, 16), (90, 16), (180, 13)], dtype=self.tasktype)
        self.task_data[23][16] = np.array([(15, 14), (20, 13), (36, 16), (60, 11), (180, 16)], dtype=self.tasktype)
        self.task_data[23][17] = np.array([(15, 11), (18, 6), (30, 21), (36, 16), (180, 15)], dtype=self.tasktype)
        self.task_data[23][18] = np.array([(12, 6), (20, 15), (36, 17), (45, 22), (180, 16)], dtype=self.tasktype)
        self.task_data[23][19] = np.array([(10, 7), (20, 11), (30, 13), (45, 23), (180, 20)], dtype=self.tasktype)
        self.task_data[24][0] = np.array([(12, 11), (15, 11), (20, 7), (45, 13), (180, 20)], dtype=self.tasktype)
        self.task_data[24][1] = np.array([(18, 14), (20, 19), (36, 13), (90, 25), (180, 6)], dtype=self.tasktype)
        self.task_data[24][2] = np.array([(10, 7), (12, 12), (45, 19), (60, 11), (180, 17)], dtype=self.tasktype)
        self.task_data[24][3] = np.array([(20, 17), (30, 22), (36, 22), (60, 6), (180, 19)], dtype=self.tasktype)
        self.task_data[24][4] = np.array([(15, 14), (30, 19), (36, 21), (90, 14), (180, 17)], dtype=self.tasktype)
        self.task_data[24][5] = np.array([(10, 9), (15, 8), (20, 17), (90, 7), (180, 9)], dtype=self.tasktype)
        self.task_data[24][6] = np.array([(15, 12), (30, 21), (45, 24), (60, 19), (180, 9)], dtype=self.tasktype)
        self.task_data[24][7] = np.array([(12, 11), (15, 14), (45, 14), (90, 18), (180, 8)], dtype=self.tasktype)
        self.task_data[24][8] = np.array([(20, 17), (30, 23), (45, 19), (90, 21), (180, 23)], dtype=self.tasktype)
        self.task_data[24][9] = np.array([(10, 6), (18, 13), (30, 16), (60, 25), (180, 25)], dtype=self.tasktype)
        self.task_data[24][10] = np.array([(18, 17), (30, 23), (36, 13), (45, 11), (180, 15)], dtype=self.tasktype)
        self.task_data[24][11] = np.array([(12, 5), (15, 14), (30, 21), (60, 17), (180, 10)], dtype=self.tasktype)
        self.task_data[24][12] = np.array([(6, 5), (10, 5), (30, 12), (36, 19), (180, 24)], dtype=self.tasktype)
        self.task_data[24][13] = np.array([(18, 8), (20, 17), (30, 23), (45, 12), (180, 15)], dtype=self.tasktype)
        self.task_data[24][14] = np.array([(9, 7), (15, 10), (18, 7), (45, 24), (180, 7)], dtype=self.tasktype)
        self.task_data[24][15] = np.array([(12, 11), (18, 17), (45, 13), (90, 13), (180, 20)], dtype=self.tasktype)
        self.task_data[24][16] = np.array([(12, 11), (20, 15), (45, 17), (90, 23), (180, 19)], dtype=self.tasktype)
        self.task_data[24][17] = np.array([(15, 14), (30, 25), (60, 18), (90, 23), (180, 14)], dtype=self.tasktype)
        self.task_data[24][18] = np.array([(12, 9), (20, 15), (30, 17), (45, 13), (180, 7)], dtype=self.tasktype)
        self.task_data[24][19] = np.array([(15, 12), (20, 11), (30, 23), (90, 13), (180, 25)], dtype=self.tasktype)
        self.task_data[25][0] = np.array([(18, 17), (20, 17), (30, 6), (36, 15), (180, 17)], dtype=self.tasktype)
        self.task_data[25][1] = np.array([(15, 13), (18, 11), (20, 11), (60, 25), (180, 10)], dtype=self.tasktype)
        self.task_data[25][2] = np.array([(12, 9), (18, 14), (36, 23), (90, 22), (180, 16)], dtype=self.tasktype)
        self.task_data[25][3] = np.array([(12, 11), (15, 13), (36, 9), (45, 17), (180, 15)], dtype=self.tasktype)
        self.task_data[25][4] = np.array([(9, 6), (18, 13), (30, 23), (90, 19), (180, 23)], dtype=self.tasktype)
        self.task_data[25][5] = np.array([(15, 14), (20, 18), (36, 7), (45, 18), (180, 14)], dtype=self.tasktype)
        self.task_data[25][6] = np.array([(15, 13), (18, 14), (20, 9), (90, 24), (180, 25)], dtype=self.tasktype)
        self.task_data[25][7] = np.array([(9, 8), (18, 11), (30, 23), (90, 9), (180, 23)], dtype=self.tasktype)
        self.task_data[25][8] = np.array([(15, 13), (18, 14), (30, 20), (60, 9), (180, 9)], dtype=self.tasktype)
        self.task_data[25][9] = np.array([(15, 13), (18, 14), (30, 6), (36, 22), (180, 8)], dtype=self.tasktype)
        self.task_data[25][10] = np.array([(12, 11), (18, 14), (36, 20), (90, 17), (180, 11)], dtype=self.tasktype)
        self.task_data[25][11] = np.array([(15, 14), (20, 17), (36, 13), (60, 19), (180, 8)], dtype=self.tasktype)
        self.task_data[25][12] = np.array([(12, 10), (15, 13), (36, 17), (60, 17), (180, 8)], dtype=self.tasktype)
        self.task_data[25][13] = np.array([(15, 14), (18, 17), (36, 16), (60, 9), (180, 6)], dtype=self.tasktype)
        self.task_data[25][14] = np.array([(18, 17), (30, 19), (45, 18), (60, 24), (180, 23)], dtype=self.tasktype)
        self.task_data[25][15] = np.array([(12, 9), (15, 14), (30, 14), (45, 13), (180, 11)], dtype=self.tasktype)
        self.task_data[25][16] = np.array([(9, 8), (15, 12), (30, 7), (45, 20), (180, 25)], dtype=self.tasktype)
        self.task_data[25][17] = np.array([(12, 9), (18, 17), (30, 17), (60, 10), (180, 14)], dtype=self.tasktype)
        self.task_data[25][18] = np.array([(9, 6), (18, 16), (30, 17), (90, 24), (180, 21)], dtype=self.tasktype)
        self.task_data[25][19] = np.array([(12, 11), (18, 13), (36, 21), (60, 9), (180, 23)], dtype=self.tasktype)
        self.task_data[26][0] = np.array([(15, 13), (20, 18), (36, 25), (60, 6), (180, 6)], dtype=self.tasktype)
        self.task_data[26][1] = np.array([(20, 20), (30, 25), (45, 23), (90, 13), (180, 21)], dtype=self.tasktype)
        self.task_data[26][2] = np.array([(10, 9), (20, 11), (30, 23), (36, 13), (180, 6)], dtype=self.tasktype)
        self.task_data[26][3] = np.array([(15, 14), (18, 7), (20, 9), (30, 23), (180, 10)], dtype=self.tasktype)
        self.task_data[26][4] = np.array([(15, 14), (18, 16), (45, 13), (60, 23), (180, 17)], dtype=self.tasktype)
        self.task_data[26][5] = np.array([(18, 15), (30, 19), (36, 20), (45, 23), (180, 12)], dtype=self.tasktype)
        self.task_data[26][6] = np.array([(9, 5), (12, 10), (18, 13), (20, 9), (180, 6)], dtype=self.tasktype)
        self.task_data[26][7] = np.array([(15, 14), (20, 13), (36, 25), (90, 17), (180, 25)], dtype=self.tasktype)
        self.task_data[26][8] = np.array([(12, 11), (20, 19), (45, 21), (60, 14), (180, 6)], dtype=self.tasktype)
        self.task_data[26][9] = np.array([(15, 11), (20, 16), (30, 25), (90, 9), (180, 25)], dtype=self.tasktype)
        self.task_data[26][10] = np.array([(6, 5), (10, 9), (12, 7), (60, 12), (180, 15)], dtype=self.tasktype)
        self.task_data[26][11] = np.array([(9, 8), (15, 14), (36, 20), (60, 11), (180, 7)], dtype=self.tasktype)
        self.task_data[26][12] = np.array([(12, 11), (15, 15), (45, 14), (60, 19), (180, 10)], dtype=self.tasktype)
        self.task_data[26][13] = np.array([(9, 8), (18, 17), (45, 23), (90, 17), (180, 14)], dtype=self.tasktype)
        self.task_data[26][14] = np.array([(15, 12), (20, 11), (30, 23), (45, 20), (180, 8)], dtype=self.tasktype)
        self.task_data[26][15] = np.array([(12, 7), (15, 12), (30, 24), (45, 14), (180, 19)], dtype=self.tasktype)
        self.task_data[26][16] = np.array([(10, 9), (18, 13), (36, 17), (45, 19), (180, 15)], dtype=self.tasktype)
        self.task_data[26][17] = np.array([(9, 8), (10, 8), (18, 6), (36, 17), (180, 19)], dtype=self.tasktype)
        self.task_data[26][18] = np.array([(15, 13), (18, 11), (36, 21), (45, 22), (180, 9)], dtype=self.tasktype)
        self.task_data[26][19] = np.array([(15, 14), (18, 17), (45, 22), (60, 8), (180, 20)], dtype=self.tasktype)
        self.task_data[27][0] = np.array([(9, 7), (12, 9), (20, 8), (30, 22), (180, 7)], dtype=self.tasktype)
        self.task_data[27][1] = np.array([(9, 7), (20, 17), (30, 22), (45, 11), (180, 16)], dtype=self.tasktype)
        self.task_data[27][2] = np.array([(12, 7), (18, 18), (30, 25), (45, 11), (180, 8)], dtype=self.tasktype)
        self.task_data[27][3] = np.array([(9, 9), (12, 11), (20, 5), (30, 15), (180, 5)], dtype=self.tasktype)
        self.task_data[27][4] = np.array([(10, 8), (15, 14), (30, 17), (36, 11), (180, 16)], dtype=self.tasktype)
        self.task_data[27][5] = np.array([(12, 11), (18, 13), (20, 17), (90, 11), (180, 16)], dtype=self.tasktype)
        self.task_data[27][6] = np.array([(6, 6), (20, 9), (30, 19), (36, 19), (180, 17)], dtype=self.tasktype)
        self.task_data[27][7] = np.array([(10, 10), (18, 13), (36, 22), (60, 19), (180, 10)], dtype=self.tasktype)
        self.task_data[27][8] = np.array([(15, 13), (18, 13), (20, 7), (30, 22), (180, 6)], dtype=self.tasktype)
        self.task_data[27][9] = np.array([(12, 11), (20, 19), (30, 18), (36, 7), (180, 7)], dtype=self.tasktype)
        self.task_data[27][10] = np.array([(12, 11), (20, 19), (45, 24), (90, 22), (180, 10)], dtype=self.tasktype)
        self.task_data[27][11] = np.array([(15, 14), (20, 12), (36, 22), (45, 21), (180, 16)], dtype=self.tasktype)
        self.task_data[27][12] = np.array([(15, 14), (20, 18), (45, 25), (90, 19), (180, 20)], dtype=self.tasktype)
        self.task_data[27][13] = np.array([(12, 9), (20, 17), (30, 17), (36, 17), (180, 11)], dtype=self.tasktype)
        self.task_data[27][14] = np.array([(15, 14), (20, 19), (36, 18), (60, 13), (180, 18)], dtype=self.tasktype)
        self.task_data[27][15] = np.array([(15, 13), (18, 14), (20, 12), (30, 11), (180, 17)], dtype=self.tasktype)
        self.task_data[27][16] = np.array([(12, 11), (15, 14), (18, 11), (30, 5), (180, 13)], dtype=self.tasktype)
        self.task_data[27][17] = np.array([(15, 14), (20, 9), (30, 23), (36, 16), (180, 19)], dtype=self.tasktype)
        self.task_data[27][18] = np.array([(12, 10), (15, 12), (20, 11), (45, 22), (180, 6)], dtype=self.tasktype)
        self.task_data[27][19] = np.array([(12, 10), (20, 17), (36, 23), (45, 14), (180, 12)], dtype=self.tasktype)
        self.task_data[28][0] = np.array([(12, 10), (15, 14), (36, 20), (45, 19), (180, 9)], dtype=self.tasktype)
        self.task_data[28][1] = np.array([(10, 8), (15, 13), (36, 25), (60, 24), (180, 9)], dtype=self.tasktype)
        self.task_data[28][2] = np.array([(15, 14), (30, 23), (36, 23), (60, 21), (180, 22)], dtype=self.tasktype)
        self.task_data[28][3] = np.array([(9, 8), (18, 15), (20, 18), (90, 11), (180, 10)], dtype=self.tasktype)
        self.task_data[28][4] = np.array([(12, 11), (18, 13), (30, 19), (36, 17), (180, 11)], dtype=self.tasktype)
        self.task_data[28][5] = np.array([(18, 11), (20, 18), (30, 23), (36, 14), (180, 23)], dtype=self.tasktype)
        self.task_data[28][6] = np.array([(6, 5), (15, 11), (36, 24), (45, 23), (180, 8)], dtype=self.tasktype)
        self.task_data[28][7] = np.array([(9, 8), (18, 14), (20, 13), (30, 13), (180, 9)], dtype=self.tasktype)
        self.task_data[28][8] = np.array([(9, 8), (15, 8), (18, 14), (45, 23), (180, 17)], dtype=self.tasktype)
        self.task_data[28][9] = np.array([(18, 17), (30, 23), (36, 23), (60, 24), (180, 8)], dtype=self.tasktype)
        self.task_data[28][10] = np.array([(10, 10), (18, 16), (20, 10), (30, 11), (180, 8)], dtype=self.tasktype)
        self.task_data[28][11] = np.array([(12, 10), (15, 9), (18, 17), (45, 13), (180, 23)], dtype=self.tasktype)
        self.task_data[28][12] = np.array([(12, 11), (15, 14), (45, 25), (60, 22), (180, 6)], dtype=self.tasktype)
        self.task_data[28][13] = np.array([(12, 7), (15, 14), (20, 16), (45, 19), (180, 11)], dtype=self.tasktype)
        self.task_data[28][14] = np.array([(9, 7), (18, 15), (30, 17), (45, 24), (180, 17)], dtype=self.tasktype)
        self.task_data[28][15] = np.array([(15, 14), (20, 19), (36, 20), (60, 14), (180, 23)], dtype=self.tasktype)
        self.task_data[28][16] = np.array([(10, 9), (20, 19), (30, 8), (36, 23), (180, 8)], dtype=self.tasktype)
        self.task_data[28][17] = np.array([(12, 11), (15, 13), (20, 14), (90, 17), (180, 25)], dtype=self.tasktype)
        self.task_data[28][18] = np.array([(12, 11), (18, 17), (30, 17), (60, 19), (180, 9)], dtype=self.tasktype)
        self.task_data[28][19] = np.array([(12, 10), (18, 13), (20, 17), (36, 10), (180, 19)], dtype=self.tasktype)
        self.task_data[29][0] = np.array([(10, 9), (18, 17), (36, 23), (45, 16), (180, 12)], dtype=self.tasktype)
        self.task_data[29][1] = np.array([(9, 8), (10, 7), (18, 17), (30, 10), (180, 7)], dtype=self.tasktype)
        self.task_data[29][2] = np.array([(12, 6), (15, 14), (18, 18), (30, 13), (180, 5)], dtype=self.tasktype)
        self.task_data[29][3] = np.array([(15, 13), (18, 12), (30, 19), (36, 25), (180, 8)], dtype=self.tasktype)
        self.task_data[29][4] = np.array([(9, 8), (18, 17), (20, 16), (60, 13), (180, 8)], dtype=self.tasktype)
        self.task_data[29][5] = np.array([(12, 11), (15, 14), (18, 13), (45, 11), (180, 14)], dtype=self.tasktype)
        self.task_data[29][6] = np.array([(10, 9), (15, 12), (30, 21), (36, 17), (180, 5)], dtype=self.tasktype)
        self.task_data[29][7] = np.array([(10, 6), (20, 19), (30, 22), (36, 21), (180, 5)], dtype=self.tasktype)
        self.task_data[29][8] = np.array([(12, 8), (18, 13), (20, 19), (45, 22), (180, 14)], dtype=self.tasktype)
        self.task_data[29][9] = np.array([(9, 8), (18, 14), (30, 19), (45, 23), (180, 17)], dtype=self.tasktype)
        self.task_data[29][10] = np.array([(9, 8), (15, 9), (30, 23), (36, 20), (180, 17)], dtype=self.tasktype)
        self.task_data[29][11] = np.array([(10, 9), (18, 13), (20, 17), (36, 14), (180, 6)], dtype=self.tasktype)
        self.task_data[29][12] = np.array([(15, 14), (18, 18), (20, 9), (30, 13), (180, 16)], dtype=self.tasktype)
        self.task_data[29][13] = np.array([(12, 6), (15, 14), (18, 17), (20, 8), (180, 23)], dtype=self.tasktype)
        self.task_data[29][14] = np.array([(9, 8), (15, 14), (18, 13), (60, 17), (180, 13)], dtype=self.tasktype)
        self.task_data[29][15] = np.array([(6, 6), (15, 13), (18, 11), (36, 11), (180, 22)], dtype=self.tasktype)
        self.task_data[29][16] = np.array([(15, 14), (18, 16), (36, 21), (45, 19), (180, 13)], dtype=self.tasktype)
        self.task_data[29][17] = np.array([(12, 8), (15, 13), (20, 14), (36, 23), (180, 6)], dtype=self.tasktype)
        self.task_data[29][18] = np.array([(15, 8), (18, 17), (30, 22), (36, 23), (180, 9)], dtype=self.tasktype)
        self.task_data[29][19] = np.array([(15, 10), (20, 19), (30, 21), (45, 23), (180, 13)], dtype=self.tasktype)

        self.task_data[30][0] = np.array([(15, 13), (18, 17), (20, 19), (90, 15), (180, 13)], dtype=self.tasktype)
        self.task_data[30][1] = np.array([(12, 8), (15, 13), (18, 16), (45, 20), (180, 23)], dtype=self.tasktype)
        self.task_data[30][2] = np.array([(12, 12), (20, 17), (30, 19), (36, 14), (180, 22)], dtype=self.tasktype)
        self.task_data[30][3] = np.array([(15, 13), (20, 13), (30, 22), (36, 25), (180, 10)], dtype=self.tasktype)
        self.task_data[30][4] = np.array([(9, 8), (12, 11), (36, 23), (45, 21), (180, 15)], dtype=self.tasktype)
        self.task_data[30][5] = np.array([(12, 11), (15, 11), (30, 24), (45, 22), (180, 11)], dtype=self.tasktype)
        self.task_data[30][6] = np.array([(9, 8), (15, 13), (20, 14), (45, 19), (180, 21)], dtype=self.tasktype)
        self.task_data[30][7] = np.array([(10, 9), (20, 14), (30, 25), (36, 17), (180, 17)], dtype=self.tasktype)
        self.task_data[30][8] = np.array([(15, 14), (18, 18), (36, 25), (90, 22), (180, 23)], dtype=self.tasktype)
        self.task_data[30][9] = np.array([(18, 16), (20, 19), (30, 17), (36, 20), (180, 7)], dtype=self.tasktype)
        self.task_data[30][10] = np.array([(12, 11), (15, 13), (18, 11), (36, 17), (180, 25)], dtype=self.tasktype)
        self.task_data[30][11] = np.array([(10, 9), (12, 11), (30, 24), (60, 21), (180, 6)], dtype=self.tasktype)
        self.task_data[30][12] = np.array([(12, 11), (15, 6), (18, 17), (20, 14), (180, 8)], dtype=self.tasktype)
        self.task_data[30][13] = np.array([(15, 13), (18, 17), (20, 14), (45, 20), (180, 9)], dtype=self.tasktype)
        self.task_data[30][14] = np.array([(10, 9), (15, 11), (20, 18), (30, 11), (180, 18)], dtype=self.tasktype)
        self.task_data[30][15] = np.array([(12, 12), (18, 17), (20, 17), (36, 5), (180, 12)], dtype=self.tasktype)
        self.task_data[30][16] = np.array([(15, 15), (20, 19), (36, 24), (60, 21), (180, 6)], dtype=self.tasktype)
        self.task_data[30][17] = np.array([(15, 14), (18, 13), (36, 25), (45, 24), (180, 22)], dtype=self.tasktype)
        self.task_data[30][18] = np.array([(9, 7), (12, 9), (18, 13), (36, 25), (180, 11)], dtype=self.tasktype)
        self.task_data[30][19] = np.array([(15, 8), (18, 17), (20, 14), (30, 23), (180, 9)], dtype=self.tasktype)
        self.task_data[31][0] = np.array([(12, 11), (15, 7), (18, 14), (20, 17), (180, 16)], dtype=self.tasktype)
        self.task_data[31][1] = np.array([(12, 11), (18, 17), (20, 13), (45, 21), (180, 22)], dtype=self.tasktype)
        self.task_data[31][2] = np.array([(15, 13), (18, 13), (20, 15), (30, 22), (180, 5)], dtype=self.tasktype)
        self.task_data[31][3] = np.array([(10, 9), (12, 9), (20, 17), (30, 17), (180, 5)], dtype=self.tasktype)
        self.task_data[31][4] = np.array([(9, 7), (12, 11), (15, 15), (60, 19), (180, 17)], dtype=self.tasktype)
        self.task_data[31][5] = np.array([(12, 11), (18, 16), (20, 20), (60, 10), (180, 23)], dtype=self.tasktype)
        self.task_data[31][6] = np.array([(15, 13), (18, 13), (20, 18), (30, 16), (180, 13)], dtype=self.tasktype)
        self.task_data[31][7] = np.array([(12, 7), (15, 14), (20, 19), (36, 21), (180, 9)], dtype=self.tasktype)
        self.task_data[31][8] = np.array([(15, 11), (18, 17), (30, 20), (36, 25), (180, 10)], dtype=self.tasktype)
        self.task_data[31][9] = np.array([(9, 8), (12, 6), (20, 20), (36, 24), (180, 8)], dtype=self.tasktype)
        self.task_data[31][10] = np.array([(9, 8), (15, 14), (20, 9), (30, 24), (180, 6)], dtype=self.tasktype)
        self.task_data[31][11] = np.array([(10, 9), (15, 12), (18, 13), (30, 19), (180, 9)], dtype=self.tasktype)
        self.task_data[31][12] = np.array([(12, 11), (15, 14), (18, 14), (45, 19), (180, 8)], dtype=self.tasktype)
        self.task_data[31][13] = np.array([(12, 11), (18, 17), (20, 19), (36, 8), (180, 13)], dtype=self.tasktype)
        self.task_data[31][14] = np.array([(9, 8), (15, 14), (20, 9), (30, 21), (180, 22)], dtype=self.tasktype)
        self.task_data[31][15] = np.array([(12, 11), (15, 10), (18, 17), (45, 24), (180, 7)], dtype=self.tasktype)
        self.task_data[31][16] = np.array([(6, 5), (9, 8), (15, 14), (36, 14), (180, 10)], dtype=self.tasktype)
        self.task_data[31][17] = np.array([(9, 8), (12, 11), (18, 14), (60, 23), (180, 23)], dtype=self.tasktype)
        self.task_data[31][18] = np.array([(18, 16), (20, 15), (30, 19), (36, 25), (180, 23)], dtype=self.tasktype)
        self.task_data[31][19] = np.array([(10, 9), (12, 11), (20, 19), (60, 18), (180, 6)], dtype=self.tasktype)
        self.task_data[32][0] = np.array([(9, 8), (15, 13), (20, 19), (36, 15), (180, 15)], dtype=self.tasktype)
        self.task_data[32][1] = np.array([(12, 11), (15, 14), (20, 19), (45, 14), (180, 15)], dtype=self.tasktype)
        self.task_data[32][2] = np.array([(15, 13), (18, 16), (20, 17), (36, 19), (180, 12)], dtype=self.tasktype)
        self.task_data[32][3] = np.array([(9, 7), (10, 9), (20, 17), (36, 20), (180, 20)], dtype=self.tasktype)
        self.task_data[32][4] = np.array([(12, 11), (15, 12), (20, 19), (36, 17), (180, 11)], dtype=self.tasktype)
        self.task_data[32][5] = np.array([(12, 10), (18, 18), (20, 12), (36, 23), (180, 23)], dtype=self.tasktype)
        self.task_data[32][6] = np.array([(10, 7), (15, 13), (20, 17), (30, 22), (180, 9)], dtype=self.tasktype)
        self.task_data[32][7] = np.array([(10, 9), (15, 11), (18, 12), (30, 23), (180, 25)], dtype=self.tasktype)
        self.task_data[32][8] = np.array([(12, 11), (15, 15), (20, 16), (36, 16), (180, 8)], dtype=self.tasktype)
        self.task_data[32][9] = np.array([(5, 5), (10, 9), (20, 11), (30, 21), (180, 9)], dtype=self.tasktype)
        self.task_data[32][10] = np.array([(12, 11), (15, 13), (20, 19), (45, 19), (180, 7)], dtype=self.tasktype)
        self.task_data[32][11] = np.array([(9, 7), (10, 9), (20, 18), (36, 21), (180, 6)], dtype=self.tasktype)
        self.task_data[32][12] = np.array([(18, 17), (20, 19), (30, 23), (45, 18), (180, 25)], dtype=self.tasktype)
        self.task_data[32][13] = np.array([(12, 11), (20, 19), (30, 21), (36, 19), (180, 18)], dtype=self.tasktype)
        self.task_data[32][14] = np.array([(9, 7), (18, 17), (20, 15), (36, 25), (180, 6)], dtype=self.tasktype)
        self.task_data[32][15] = np.array([(15, 13), (18, 17), (20, 15), (36, 22), (180, 5)], dtype=self.tasktype)
        self.task_data[32][16] = np.array([(12, 10), (15, 12), (20, 19), (45, 23), (180, 19)], dtype=self.tasktype)
        self.task_data[32][17] = np.array([(10, 7), (20, 19), (30, 24), (36, 24), (180, 16)], dtype=self.tasktype)
        self.task_data[32][18] = np.array([(9, 5), (12, 11), (18, 17), (30, 22), (180, 9)], dtype=self.tasktype)
        self.task_data[32][19] = np.array([(12, 11), (18, 14), (20, 14), (30, 21), (180, 18)], dtype=self.tasktype)

class DAGTaskGenerator:
    """Randomly generate several DAG tasks by uunifast algorithm.

    """

    def __init__(self, seed: int, n: int = 5, uti: float = 3.0, p: float = 0.2,
                 node_min: int = 10, node_max: int = 30,
                 mode: str = 'SIM') -> None:
        """
        Args:
        ---
            seed (int): random seed
            n (int, optional): number of tasks in the taskset. Defaults to 5.
            uti (float, optional): total utilization. Defaults to 3.0.
            p (float, optional): edge probability. Defaults to 0.2.
        """
        self.n = n; self.uti = uti; self.edge_prob = p
        self.U = np.zeros(n, dtype=float)

        self.width = 5 # maximum of nodes in one layer
        self.node_min = node_min; self.node_max = node_max
        
        np.random.seed(seed)
        self.seed = seed
        
        # enum constant, consistent with cpp src
        CPU = 0; DataCopy = 3; GPU = 7; FPGA = 8; UNKNOWN = 9
        
        self.proc_type = 10
        self.avail_procs = np.zeros(self.proc_type, dtype=bool)

        if mode == 'SIM':
            self.avail_procs[CPU] = True
            self.avail_procs[DataCopy] = True
            self.avail_procs[GPU] = True
            self.avail_proc_list = [CPU, DataCopy, GPU]
        
            self.transition_prob = np.zeros((self.proc_type,self.proc_type), dtype=float)
            self.transition_prob[CPU][CPU] = 0.3
            self.transition_prob[CPU][DataCopy] = 0.7
            self.transition_prob[DataCopy][DataCopy] = 0.3
            self.transition_prob[DataCopy][CPU] = 0.35
            self.transition_prob[DataCopy][GPU] = 0.35
            self.transition_prob[GPU][GPU] = 0.3
            self.transition_prob[GPU][DataCopy] = 0.7
        else:
            self.avail_procs[CPU] = True
            self.avail_procs[GPU] = True
            self.avail_proc_list = [CPU, GPU]
        
            self.transition_prob = np.zeros((self.proc_type,self.proc_type), dtype=float)
            self.transition_prob[CPU][CPU] = 0.3
            self.transition_prob[CPU][GPU] = 0.7
            self.transition_prob[GPU][GPU] = 0.3
            self.transition_prob[GPU][CPU] = 0.7
        
        # describe the range of each kind proc
        self.seg_min = np.ones(self.proc_type, dtype=int)
        self.seg_max = np.ones(self.proc_type, dtype=int) * 10
        
        # self.seg_max[DataCopy] = 20
    
    def generate_utilizations(self):
        """ Generate utilization by UUniFast, stored in self.U
        """
        
        from numpy.random import randint
        np.random.seed(self.seed+63175)
        while True:
            valid = 1
            for ui in range(self.n):
                self.U[ui] = float(randint(1, 100))
            resolution: float = np.sum(self.U) / self.uti
        
            for ui in range(self.n):
                self.U[ui] = self.U[ui] / resolution
                if self.U[ui] > (self.uti * 0.8):
                    valid = 0
            if valid == 1:
                break

    def generate_dag_task(self, uti=1.0) -> list:
        """ Generate segments and dependencies for one dag task
        
        Returns:
        ---
            list:  [period, num_nodes, num_edges,
                   (s1,t1), (s2,t2), ...
                   (u1,v1), (u2,v2), ...
            ]
        """
        from numpy.random import randint
        num_nodes = randint(self.node_min, self.node_max + 1)
        nodes = np.zeros(num_nodes, dtype=int)
        types = np.ones(num_nodes, dtype=int) * 9
        
        # The first and last node must be CPU
        nodes[0] = randint(self.seg_min[0], self.seg_max[0]+1)
        nodes[-1] = randint(self.seg_min[0], self.seg_max[0]+1)
        types[0] = 0; types[-1] = 0
   
        nodes_remain = num_nodes - 2
        cuts = []
        
        while nodes_remain > 0:
            nodes_current = randint(2, min(self.width, nodes_remain)+1)
            if nodes_current +1 == nodes_remain: continue
            cuts.append(nodes_current)
            nodes_remain = nodes_remain - nodes_current
        
        cuts = np.array(cuts); np.random.shuffle(cuts)
        
        prec = np.zeros(num_nodes, dtype=bool)
        index = 1
        
        edges = []
        for g, cut in enumerate(cuts):
            for i in range(index, index + cut):
                if prec[i] == False:
                    prec_node = randint(0, index)
                    types[i] = np.random.choice(range(self.proc_type), p=self.transition_prob[types[prec_node]])
                    nodes[i] = randint(self.seg_min[types[0]], self.seg_max[types[0]]+1)
                    edges += [prec_node, i]
                    prec[i] = True
                if g != len(cuts) - 1:
                    for j in range(index + cut, index + cut + cuts[g+1]):
                        if np.random.rand() < self.edge_prob:
                            edges += [i,j]
                            if prec[j] == False:
                                prec[j] = True
                                types[j] = np.random.choice(range(self.proc_type), p=self.transition_prob[types[i]])
                                nodes[j] = randint(self.seg_min[types[i]], self.seg_max[types[i]]+1)
                else:
                    edges += [i, num_nodes-1]
            index = index + cut
        
        result = [int(np.sum(nodes) / uti), num_nodes, len(edges)//2]
        for i in range(num_nodes):
            result += [int(nodes[i]), int(types[i])]
        
        result += edges
        return result
    
    def generate_tasksets(self):
        self.generate_utilizations()
        
        res = []
        for uti in self.U:
            res.append(self.generate_dag_task(uti))
        
        self.task_sets = res
        return res

class DAGViTGenerator:
    """Randomly generate several DAG ViT tasks by uunifast algorithm.

    """

    def __init__(self, seed: int, n: int = 5, uti: float = 3.0) -> None:
        """
        Args:
        ---
            seed (int): random seed
            n (int, optional): number of tasks in the taskset. Defaults to 5.
            uti (float, optional): total utilization. Defaults to 3.0.
            p (float, optional): edge probability. Defaults to 0.2.
        """
        self.n = n; self.uti = uti
        self.U = np.zeros(n, dtype=float)

 
        np.random.seed(seed)
        self.seed = seed
        
        # enum constant, consistent with cpp src
        CPU = 0; DataCopy = 3; GPU = 7; FPGA = 8; UNKNOWN = 9
        
        self.proc_type = 10
        self.avail_procs = np.zeros(self.proc_type, dtype=bool)


        self.avail_procs[CPU] = True
        self.avail_procs[GPU] = True
        self.avail_proc_list = [CPU, GPU]
        
    
        
        # self.seg_max[DataCopy] = 20
    
    def generate_utilizations(self):
        """ Generate utilization by UUniFast, stored in self.U
        """
        np.random.seed(self.seed+19742)
        from numpy.random import randint
        while True:
            valid = 1
            for ui in range(self.n):
                self.U[ui] = float(randint(1, 100))
            resolution: float = np.sum(self.U) / self.uti
        
            for ui in range(self.n):
                self.U[ui] = self.U[ui] / resolution
                if self.U[ui] >= 0.9:
                    valid = 0
            if valid == 1:
                break
    
    def generate_tasksets(self):
        self.generate_utilizations()
        
        """
            list:  [period, num_nodes, num_edges,
                   s1,t1, s2,t2, ...
                   u1,v1, u2,v2, ...
            ]
        """

        res = []
        dependency = [ 0,1, 1,2, 2,3, 2,4, 2,5, 3,6, 4,6, 5,7, 6,7,
                       7,8, 8,9, 9,10, 10,11, 11,12]
        num_nodes = 13; num_edges = len(dependency)
        tasks = np.zeros((5,13), dtype=list)
        tasks[0] = np.array([6,2,1,1,1,1,1,3,1,1,4,1,2]) #25
        tasks[1] = np.array([19,5,2,1,1,1,4,8,3,2,9,1,2]) #58
        tasks[2] = np.array([56,8,4,2,2,1,12,17,4,3,11,3,3]) #126
        tasks[3] = np.array([119,29,3,3,3,3,15,30,4,9,12,8,4]) #242
        tasks[4] = np.array([147,88,4,9,9,9,30,59,4,30,23,29,6]) #447
        types = [0,7,0,7,7,7,7,7,0,7,0,7,0]

        for i in range(5):
            tmp = [int(np.sum(tasks[i]) / self.U[i]), num_nodes, num_edges]
            for j in range(num_nodes):
                tmp += [int(tasks[i][j]), types[j]]
            tmp += dependency
            res.append(tmp)
        
        self.task_sets = res
        return res

if __name__ == "__main__":
    g = DAGTaskGenerator(13, uti=3.5)
    print(g.generate_dag_task())
