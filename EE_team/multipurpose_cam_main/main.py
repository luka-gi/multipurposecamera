import sys
import argparse
import subsys0_1,subsys0_3,full_system

if __name__ == "__main__":  
    parser = argparse.ArgumentParser(description='Args for multipurposecamera script. All false by default')
    parser.add_argument('-v','--verbose', action='store_true', help='verbose output')
    parser.add_argument('-o','--display', action='store_true', help='output display images to monitor')
    parser.add_argument('-p','--process', action='store_true', help='process using openpose (default off to save memory)')
    parser.add_argument('-w','--write', action='store_true', help='save images to disk')
    parser.add_argument('-a','--all', action='store_true', help='enable all options')
    parser.add_argument('-s','--subsystem',type=int, help="specify subsystem to test (0 = all or highest level)",nargs='?', const=1, default=0)
    parser.add_argument('-d','--device', type=int, help='specify device number',nargs='?', const=1, default=3)

    args = parser.parse_args()

    displaymode = args.display or args.all
    verbose = args.verbose or args.all
    run_openpose = args.process or args.all
    write_images = args.write or args.all
    openpose_device_id = args.device
    subsystem_to_test = args.subsystem

    if (subsystem_to_test == 1 or subsystem_to_test == 2 or subsystem_to_test == 3 or subsystem_to_test == 4 or subsystem_to_test == 5 or subsystem_to_test == 6):
        print("\nTesting subsystem",subsystem_to_test)
    elif (subsystem_to_test == 0):
        print("\nTesting high level main system")
    else:
        print("\nInvalid argument for subsystem\n")
        sys.exit()

    if not (openpose_device_id == 3 or openpose_device_id == 4):
        print("\nDevice ID not valid. --device 3 for stereo left and --device 4 for stereo right.\n(check device settings or restart in case this changed)\n")
        sys.exit()

    if verbose:
        print("\nrunning with arguments:\n")
        print("verbose =",verbose)
        print("display =",displaymode)
        print("process =",run_openpose)
        print("write =",write_images)
        print("using device /dev/video"+str(openpose_device_id))

    if not (verbose or displaymode or run_openpose or write_images or args.all):
        print("\n=====================================================================")
        print("  WARN: you have not run the module with any args. see list with -h")
        print("=====================================================================")

    print("\nPlease ensure that you are only running this from the bash script. Python version should be 3.6.9")
    print("Python version: "+str(sys.version_info.major)+"."+str(sys.version_info.minor)+"."+str(sys.version_info.micro)+"\n")

    # args to pass into subfunctions
    args = (displaymode,verbose,run_openpose,write_images,openpose_device_id)

    if subsystem_to_test == 0:
        full_system.run(*args)
    if subsystem_to_test == 1:
        subsys0_1.run(*args)
    if subsystem_to_test == 2:
        print()
    if subsystem_to_test == 3:
        subsys0_3.run(*args)
    if subsystem_to_test == 4:
        print()
    if subsystem_to_test == 5:
        print()
    if subsystem_to_test == 6:
        print()
