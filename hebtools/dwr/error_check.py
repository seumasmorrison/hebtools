import numpy as np
import pandas as pd

def check(extrema_df, sigma = 4):
     
    directions = ['heave','north','west']
    std_factor = {}
    suf = '_file_std'
    
    def detect_error_waves(extrema_df):
        """Find values with status signal problem and is a peak or trough,
        then adds a 'signal_error' boolean column to the DataFrame
        """
        print "start detect_error_waves"
        error_wave_mask = extrema_df['sig_qual']>0
        extrema_df['signal_error'] = error_wave_mask
        extrems_plus_errors = extrema_df.sort()
        return extrems_plus_errors
    
    def compare_std(raw_plus_std, direction):
        return raw_plus_std[direction].abs() > \
               (raw_plus_std[direction + suf] * sigma)
    
    def detect_4_by_std(sigma, displacements):
        """This function groups the displacements in the DataFrame by filename
        getting the standard deviation for each displacement (heave,north,west) 
        The displacements are then compared against 4 times 
        their standard deviation and any records exceeding this comparison for 
        any displacement are given a True value for >4*std column, the standard
        deviations are also stored in the DataFrame so further comparison can
        be made
        """
        print "detect_4_by_std"
        four_times_std_heave_30_mins = []
        filtered_displacements = displacements[displacements['signal_error']==0]
        #filtered_displacements = displacements
        grouped_displacements = filtered_displacements.groupby('file_name')
        standard_deviations = grouped_displacements['heave','north','west'].std()
        raw_plus_std = displacements.join(standard_deviations, 
                                                          on='file_name', 
                                                          rsuffix='_file_std')                                
        std_list = {}
        for direction in directions:
           std_list = compare_std(raw_plus_std, direction)
        disp_more_than_4_std = std_list[0] + std_list[1] + std_list[2]
        raw_plus_std['>4*std'] = disp_more_than_4_std
        raw_plus_std.save('raw_plus_std')
        return raw_plus_std
        
    def compare_factors(main_factor, second_factor, third_factor):
        """ return mask of one displacement where its displacements are the 
        largest """
        return main_factor[(main_factor > second_factor) & \
                           (main_factor > third_factor)]
    
    def calc_std_factor(raw_plus_std):
        for direction in directions:
            std_factor[direction] = (raw_plus_std[direction] /
                                     raw_plus_std[direction + suf]).abs()
        factors = []
        dirs = directions[:]
        for direction in directions:
            factors.append(compare_factors(std_factor[dirs[0]], 
                                           std_factor[dirs[1]],
                                           std_factor[dirs[2]]))
            dirs.append(dirs.pop(0))
        combined_factors = pd.concat(factors)
        combined_factors.name = 'max_std_factor'
        raw_plus_std = raw_plus_std.join(combined_factors)
        raw_plus_std.save('raw_plus_std')
        return raw_plus_std
        
    displacements = detect_error_waves(extrema_df)
    raw_plus_std = detect_4_by_std(sigma, displacements)
    return calc_std_factor(raw_plus_std)