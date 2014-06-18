from numpy import dtype, array

class FocusInfo:
    
    @staticmethod
    def create_focus_info(positions, displacements):
        num_pos = len(positions)
        num_disp = len(displacements)
        assert num_pos == num_disp
        
        infos = [0]*num_disp
        for k in range(num_disp):
            infos[k] = FocusInfo(positions[k], displacements[k])
            
        return infos
    
    def __init__(self, position, displacement):
        self.position = array(position, dtype=dtype(float))
        self.displacement = array(displacement, dtype=dtype(float))