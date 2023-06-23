# HBIO Processing Module
# Read in .txt files, create force time curves, reformat to .csv file

# Import packages


# Define the function
def force_csv():
    """
    Function::: force_csv
        Description: Read in .txt files, create force time curves, reformat to .csv file
        Details:
            - Read in .txt files
            - Create force time curves
            - Reformat to .csv file
    Inputs
        - None
    Outputs
        - None
    """

    import os
    import pandas as pd
    import matplotlib.pyplot as plt


    # Import custom functions
    from ImportForce_TXT import ImportForce_TXT

    # Make a list of the folders
    folders = ['squat', 'marching', 'sprint', 'walk']

    for i in range(len(folders)):


        # Define the directory
        dir = r'C:\Users\hestewar\Desktop\230322_hbio401' + '\\' + folders[i]

        # Create a force time curve for each file in directory
        for file in os.listdir(dir):
            if file.endswith('.txt'):
                # Import the force data from the .txt file
                # get the full file name
                file_full = os.path.join(dir, file)
                data_f1_raw, samp_force, _ = ImportForce_TXT(file_full)

                # Find the names of all the force plates in the file before the space
                fp_full_names = [col for col in data_f1_raw.columns if 'Fz' in col]

                # Reduce to only include the name before the space
                fp_names = [fp.split(' ')[0] for fp in fp_full_names]

                # Rename the columns to FP1_Fx, FP1_Fy, FP1_Fz, FP2_Fx, FP2_Fy, FP2_Fz, Time
                # Attila columns become FP1
                # Ryan columns become FP2
                data_f1_raw.columns = ['Time','FP1_Fx', 'FP1_Fy', 'FP1_Fz', 'FP1_Ax', 'FP1_Ay',
                                       'FP2_Fx', 'FP2_Fy', 'FP2_Fz', 'FP2_Ax', 'FP2_Ay']

                # Flip the Fy columns
                data_f1_raw['FP1_Fy'] = -data_f1_raw['FP1_Fy']
                data_f1_raw['FP2_Fy'] = -data_f1_raw['FP2_Fy']

                # Plot the data in matplotlib and open in a window
                # Make 3 subplots for FP1, FP2, and combined
                fig, ax = plt.subplots(3, 1, sharex=True)

                # Subplot 1: FP1
                ax[0].plot(data_f1_raw['Time'], data_f1_raw['FP1_Fx'], label='FP1_Fx')
                ax[0].plot(data_f1_raw['Time'], data_f1_raw['FP1_Fy'], label='FP1_Fy')
                ax[0].plot(data_f1_raw['Time'], data_f1_raw['FP1_Fz'], label='FP1_Fz')
                ax[0].legend()

                # Subplot 2: FP2
                ax[1].plot(data_f1_raw['Time'], data_f1_raw['FP2_Fx'], label='FP2_Fx')
                ax[1].plot(data_f1_raw['Time'], data_f1_raw['FP2_Fy'], label='FP2_Fy')
                ax[1].plot(data_f1_raw['Time'], data_f1_raw['FP2_Fz'], label='FP2_Fz')
                ax[1].legend()

                # Subplot 3: Combined
                ax[2].plot(data_f1_raw['Time'], data_f1_raw['FP1_Fx']+data_f1_raw['FP2_Fx'], label='Fx Combined')
                ax[2].plot(data_f1_raw['Time'], data_f1_raw['FP1_Fy']+data_f1_raw['FP2_Fy'], label='Fy Combined')
                ax[2].plot(data_f1_raw['Time'], data_f1_raw['FP1_Fz']+data_f1_raw['FP2_Fz'], label='Fz Combined')
                ax[2].legend()

                # Set the x-axis label
                ax[2].set_xlabel('Time (s)')
                plt.show()

                # set the y-axis label
                ax[0].set_ylabel('Force (N)')
                ax[1].set_ylabel('Force (N)')
                ax[2].set_ylabel('Force (N)')

                # Set the title
                fig.suptitle(file[:-4])

                # set y-axis limits
                # find the max force combined
                max_force = max(data_f1_raw['FP1_Fz']+data_f1_raw['FP2_Fz'])

                ax[0].set_ylim(-max_force, max_force)
                ax[1].set_ylim(-max_force, max_force)
                ax[2].set_ylim(-max_force, max_force)

                # set the subtitles
                ax[0].set_title('FP1')
                ax[1].set_title('FP2')
                ax[2].set_title('Combined')


                # Save the dataframe as a .csv file to the same folder
                data_f1_raw.to_csv(os.path.join(dir,file[:-4] + '.csv'), index=False)

                # Save the figure as a .png file to the same folder
                fig.savefig(os.path.join(dir,file[:-4] + '.png'), dpi=300)

                # close the figure
                plt.close(fig)



