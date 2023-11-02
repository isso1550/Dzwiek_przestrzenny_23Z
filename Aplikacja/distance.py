from pedalboard import Pedalboard, Chorus, Reverb, Gain, HighShelfFilter, LowShelfFilter
from pedalboard.io import AudioFile
import numpy as np

def DistanceByGain(infile, outfile, distance):
    gain_change = np.log2(distance)*(-6)
    board = Pedalboard([ Gain(gain_db=gain_change)])
    with AudioFile(infile) as f:
        with AudioFile(outfile, 'w', f.samplerate, f.num_channels) as o:
            while f.tell() < f.frames:
                chunk = f.read(f.samplerate)
                effected = board(chunk, f.samplerate, reset=False)
                o.write(effected)

def DistanceByGainHighshelf(infile, outfile, distance):
    gain_change = np.log2(distance)*(-6)
    #print(f"gain_change = {gain_change}")

    #board = Pedalboard([HighShelfFilter(cutoff_frequency_hz=200, gain_db=gain_change/2), Gain(gain_db=gain_change)])
    board = Pedalboard([LowShelfFilter(cutoff_frequency_hz=200, gain_db=-gain_change/2), Gain(gain_db=gain_change)])
    with AudioFile(infile) as f:
        with AudioFile(outfile, 'w', f.samplerate, f.num_channels) as o:
            while f.tell() < f.frames:
                chunk = f.read(f.samplerate)
                effected = board(chunk, f.samplerate, reset=False)
                o.write(effected)
    


def ProgressiveDistanceByGain(infile, outfile, step_dist_change, full_iteration_dur):
    room_size = 1.0
    damping = 1.0
    wet_level = 0.83
    dry_level = 1.0
    width = 1.0
    freeze_mode = 0.0
    board = Pedalboard([Reverb(room_size, damping, wet_level, dry_level, width, freeze_mode), Gain(gain_db=0)])
    with AudioFile(infile) as f:
        len_sec = f.frames/f.samplerate
        
        print(1+(step_dist_change*full_iteration_dur/2))

        max_dist = int(step_dist_change*full_iteration_dur/2) + 1
        n_steps = full_iteration_dur/2

        distances = np.arange(1, max_dist, step_dist_change)
        print(distances)
        distances2 = np.flip(distances)
        distances = np.concatenate((distances,distances2))
        distances = np.tile(distances, int(np.ceil(len_sec/full_iteration_dur))+1)

        room = np.arange(0, 1.0, 1/n_steps)
        print(room)
        room2 = np.flip(room)
        room = np.concatenate((room, room2))
        room = np.tile(room,int(np.ceil(len_sec/full_iteration_dur))+1)

        wet = np.arange(0, 1.0, 1/n_steps)
        wet2 = np.flip(wet)
        wet = np.concatenate((wet, wet2))
        wet = np.tile(wet,int(np.ceil(len_sec/full_iteration_dur))+1)

        print(len(distances))
        print(n_steps)
        print(len(wet))

        with AudioFile(outfile, 'w', f.samplerate, f.num_channels) as o:
            i = 0
            while f.tell() < f.frames:
                chunk = f.read(f.samplerate)
                distance = distances[i]
                i = i+1
                gain_change = np.sqrt(distance)*(-6)

                board[0].room_size = room[i]
                board[0].wet_level = wet[i]
                board[1].gain_db = gain_change
                effected = board(chunk, f.samplerate, reset=False)
                o.write(effected)
        
def DistanceWithReverb(infile, outfile, distance):
    from pedalboard import Pedalboard, Reverb, Gain, LowpassFilter, HighShelfFilter, LowShelfFilter, HighpassFilter
    from pedalboard.io import AudioFile
    import numpy as np

    # Make a Pedalboard object, containing multiple audio plugins:
    room_size = 0.0
    damping = 0.25
    wet_level = 0.5
    dry_level = 1.0
    width = 1.0
    freeze_mode = 0.0

    gain_change = np.log2(distance)*(-6)
    # Reverb(room_size, damping, wet_level, dry_level, width, freeze_mode), 
    board = Pedalboard([Reverb(room_size, damping, wet_level, dry_level, width, freeze_mode),LowShelfFilter(cutoff_frequency_hz=200, gain_db=-gain_change/2), Gain(gain_db=gain_change)])
    #board = Pedalboard([HighShelfFilter(cutoff_frequency_hz=200, gain_db=-10), Gain(gain_db=-10.0)])
    #board = Pedalboard([Gain(gain_db=-10.0)])

    # Open an audio file for reading, just like a regular file:
    with AudioFile(infile) as f:
    
        # Open an audio file to write to:
        with AudioFile(outfile, 'w', f.samplerate, f.num_channels) as o:
            while f.tell() < f.frames:
                chunk = f.read(f.samplerate)
                effected = board(chunk, f.samplerate, reset=False)
                
                # Write the output to our output file:
                o.write(effected)