import pygame
import os
import re
from colorama import Fore, Style, init

##############################################################################################
# Input variables
CFD_folder = '2 - PostProcessing'   # Directory in which the output of the CFDs are located
figure_folder = '0_Figures'         # Name of the folder within 'CFD_folder', which contains the folders in which the figures are located
screen_scaling_factor = 1           # Windows setting in settings->system->display->resizing and layout %/100

##############################################################################################

# Initialize colorama
init(autoreset=True)

def load_images(directory):
    images = []
    for filename in os.listdir(directory):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            path = os.path.join(directory, filename)
            image = pygame.image.load(path)
            images.append((filename, image))
    return images

def extract_number(filename):
    # Extract the numeric part of the filename
    match = re.search(r'\d+', filename)
    return int(match.group()) if match else float('inf')

def main():
    pygame.init()

    images_A = load_images(dir_A_figures)
    images_B = load_images(dir_B_figures)

    images_A.sort(key=lambda x: extract_number(x[0]))  # Order the file based on the number in the filename
    images_B.sort(key=lambda x: extract_number(x[0]))

    current_index_A = 0
    current_index_B = 0

    scaling_factor = screen_scaling_factor
    max_resolution = pygame.display.list_modes()[0]
    screen_size = (int(max_resolution[0] / scaling_factor), int(max_resolution[1] / scaling_factor))
    screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)

    font = pygame.font.Font(None, 36)

    running = True
    key_down_q = False

    while running:
        screen.fill((255, 255, 255))

        if not key_down_q:
            current_image_A = images_A[current_index_A][1]
            screen.blit(pygame.transform.scale(current_image_A, screen_size), (0, 0))
            current_info = sim1 + '-' + images_A[current_index_A][0]
        else:
            current_image_B = images_B[current_index_B][1]
            screen.blit(pygame.transform.scale(current_image_B, screen_size), (0, 0))
            current_info = sim2 + '-' + images_B[current_index_B][0]

        draw_text(screen, f"{current_info}", font, (0, 0, 0), (10, screen.get_height() - 40))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif not key_down_q:
                    if event.key == pygame.K_RIGHT:
                        current_index_A = (current_index_A + 1) % len(images_A)
                    elif event.key == pygame.K_LEFT:
                        current_index_A = (current_index_A - 1) % len(images_A)
                    elif event.key == pygame.K_q:
                        key_down_q = True
                        current_index_B = current_index_A
                else:
                    if event.key == pygame.K_q:
                        key_down_q = False
                        current_index_A = current_index_B
                    elif event.key == pygame.K_RIGHT:
                        current_index_B = (current_index_B + 1) % len(images_B)
                    elif event.key == pygame.K_LEFT:
                        current_index_B = (current_index_B - 1) % len(images_B)

    pygame.quit()

def draw_text(surface, text, font, color, position):
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, position)


# Get the directory of the current script
script_directory = os.path.dirname(os.path.abspath(__file__))

# Change the current working directory to the script directory
os.chdir(script_directory)


##############################################################################################
# This section is used to save the directory where the file is located and to 
# select the two CFDs to be compared
# Get the full path to the running file
file_path = os.path.abspath(__file__)

# Get the directory where the file is located
directory = os.path.dirname(file_path)

# I will move to folder "CFD_folder" where the CFD results are.
dir_A = os.path.join(directory, CFD_folder)
dir_B = os.path.join(directory, CFD_folder)

print()

# Get a list of all items (files and folders) in the specified directory
all_items = os.listdir(dir_A)

# Filter out only the folders from the list of simulations
folders = [item for item in all_items if os.path.isdir(os.path.join(dir_A, item))]

# Define a function that prompts the user for folders/simulations to open
def load_cases(folders):
    # Print the names of the folders so to have a faster understanding of the folders inside "CFD_folder"
    print(Fore.RED + "Folders available:" + Style.RESET_ALL)
    for folder in folders:
        print(Fore.YELLOW + folder + Style.RESET_ALL)
    print()
    # Ask the used for the 2 cfd to compare
    sim1 = input(Fore.CYAN + "Choose the first folder: " + Style.RESET_ALL)
    sim2 = input(Fore.CYAN + "Choose the second folder: " + Style.RESET_ALL)
    # Directory of folders where the images are located
    dir_A_base = os.path.join(dir_A, sim1, figure_folder)
    dir_B_base = os.path.join(dir_B, sim2, figure_folder)
    return(sim1, sim2, dir_A_base, dir_B_base)


##############################################################################################
# Function that shows the user the non-empty folders inside dir_A_base and dir_B_base and ask
# the user which pictures to open. The folders that will be showed to the user are only the
# ones in which there are files inside in both direcotries
def available_options(dir_A_base, dir_B_base):
    all_items_A = os.listdir(dir_A_base)
    non_empty_folders_A = [item for item in all_items_A if os.path.isdir(os.path.join(dir_A_base, item)) and any(os.listdir(os.path.join(dir_A_base, item)))]
    all_items_B = os.listdir(dir_B_base)
    non_empty_folders_B = [item for item in all_items_B if os.path.isdir(os.path.join(dir_B_base, item)) and any(os.listdir(os.path.join(dir_B_base, item)))]
    common_folders = [folder for folder in non_empty_folders_A if folder in non_empty_folders_B]
    print(Fore.RED + "Available options:" + Style.RESET_ALL)
    print(Fore.YELLOW + '0: Close' + Style.RESET_ALL)
    for number, string in enumerate(common_folders):
        print(Fore.YELLOW + f"{number+1}: {string}" + Style.RESET_ALL)
    print(Fore.YELLOW + "99: Select new folders" + Style.RESET_ALL)
    return(common_folders)


##############################################################################################
# I make sure that on the first ESC it asks me for the slice again while on the second
# one it has to stop the code
running = True

[sim1, sim2, dir_A_base, dir_B_base] = load_cases(folders)
while running:
    print()
    # Print the available options on the screen
    common_folders = available_options(dir_A_base, dir_B_base)

    # Ask the user to enter a number
    user_number = int(input(Fore.CYAN + "What do you want to see (number): " + Style.RESET_ALL))

    # If 0, it asks for other folders or quit the code; otherwise it keeps asking what to see
    if user_number == 0:
        running = False
    elif user_number == 99:
        print('#################################################################')
        print()
        [sim1, sim2, dir_A_base, dir_B_base] = load_cases(folders)
    else:
        corresponding_string = common_folders[user_number-1]
        # Directory of the two folders to open
        dir_A_figures = os.path.join(dir_A_base, corresponding_string)
        dir_B_figures = os.path.join(dir_B_base, corresponding_string)

        # Function to see the images
        main()

        print('#################################################################')