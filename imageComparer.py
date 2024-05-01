import pygame
import os
import re
from colorama import Fore, Style, init

# Input variables
CFD_folder = '2 - PostProcessing'   # Directory in which the output of the CFDs are located
figure_folder = '0_Figures'         # Name of the folder within 'CFD_folder', which contains the folders in which the figures are located
screen_scaling_factor = 1           # Windows setting in settings->system->display->resizing and layout %/100

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

    # Load images
    images_A = load_images(dir_A_figures)
    images_B = load_images(dir_B_figures)

    images_A.sort(key=lambda x: extract_number(x[0]))  # Order the files based on the number in the filename
    images_B.sort(key=lambda x: extract_number(x[0]))

    # Initialize variables
    current_index_A = 0
    current_index_B = 0
    scaling_factor = screen_scaling_factor
    max_resolution = pygame.display.list_modes()[0]
    screen_size = (int(max_resolution[0] / scaling_factor), int(max_resolution[1] / scaling_factor))
    screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)
    font = pygame.font.Font(None, 36)
    running = True
    key_down_q = False
    arrow_key_pressed = None
    zoom_level = 1.0
    default_zoom_level = 1.0
    default_image_position_x = 0
    default_image_position_y = 0
    dragging = False
    prev_mouse_pos = None
    image_position_x = 0  # Initialize image position variables
    image_position_y = 0

    # Initialize timer variables
    arrow_key_timer = 0
    arrow_key_delay = 500  # Delay in milliseconds before continuous image display starts
    continuous_scroll_timer = 0
    continuous_scroll_delay = 200  # Delay in milliseconds for continuous scrolling 

    while running:
        screen.fill((255, 255, 255))

        # Display current image
        if not key_down_q:
            current_image_A = images_A[current_index_A][1]
            scaled_image_A = pygame.transform.smoothscale(current_image_A, (int(screen.get_width() * zoom_level), int(screen.get_height() * zoom_level)))  # Scale image to fit screen
            screen.blit(scaled_image_A, (image_position_x, image_position_y))  # Adjust position based on mouse movement
            current_info = sim1 + '-' + images_A[current_index_A][0]
        else:
            current_image_B = images_B[current_index_B][1]
            scaled_image_B = pygame.transform.smoothscale(current_image_B, (int(screen.get_width() * zoom_level), int(screen.get_height() * zoom_level)))  # Scale image to fit screen
            screen.blit(scaled_image_B, (image_position_x, image_position_y))  # Adjust position based on mouse movement
            current_info = sim2 + '-' + images_B[current_index_B][0]

        # Display current image information
        draw_text(screen, f"{current_info}", font, (0, 0, 0), (10, screen.get_height() - 40))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_z:
                    # Reset zoom level to default and center image on screen
                    zoom_level = default_zoom_level  
                    default_scaled_image_A = pygame.transform.smoothscale(current_image_A, (int(screen.get_width() * default_zoom_level), int(screen.get_height() * default_zoom_level)))  # Scale image to default zoom
                    image_position_x = default_image_position_x + (screen.get_width() - default_scaled_image_A.get_width()) // 2
                    image_position_y = default_image_position_y + (screen.get_height() - default_scaled_image_A.get_height()) // 2
                    arrow_key_pressed = None
                elif event.key == pygame.K_a:
                    # Press this key after the arrow to move faster between the images
                    tmp = 0
                elif not key_down_q:
                    if event.key == pygame.K_RIGHT:
                        # Start the timer when the arrow key is pressed
                        arrow_key_pressed = pygame.K_RIGHT
                        arrow_key_timer = pygame.time.get_ticks()
                    elif event.key == pygame.K_LEFT:
                        arrow_key_pressed = pygame.K_LEFT
                        arrow_key_timer = pygame.time.get_ticks()
                    elif event.key == pygame.K_q:
                        key_down_q = True
                        current_index_B = current_index_A
                        arrow_key_pressed = None
                else:
                    if event.key == pygame.K_q:
                        key_down_q = False
                        current_index_A = current_index_B
                        arrow_key_pressed = None
                    elif event.key == pygame.K_z:
                        arrow_key_pressed = None
                    elif event.key == pygame.K_RIGHT:
                        arrow_key_pressed = pygame.K_RIGHT
                        arrow_key_timer = pygame.time.get_ticks()
                    elif event.key == pygame.K_LEFT:
                        arrow_key_pressed = pygame.K_LEFT
                        arrow_key_timer = pygame.time.get_ticks()
            elif event.type == pygame.KEYUP:
                if event.key == arrow_key_pressed:
                    arrow_key_pressed = None  # Reset the arrow key flag when released
                    arrow_key_timer = 0  # Reset the timer
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    dragging = True
                    prev_mouse_pos = event.pos
                elif event.button == 4:  # Scroll up
                    zoom_level += 0.1
                elif event.button == 5:  # Scroll down
                    zoom_level -= 0.1
                    zoom_level = max(0.1, zoom_level)  # Ensure zoom level doesn't go below 0.1
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left mouse button
                    dragging = False
            elif event.type == pygame.MOUSEMOTION:
                if dragging:
                    mouse_pos = event.pos
                    if prev_mouse_pos:
                        dx = mouse_pos[0] - prev_mouse_pos[0]
                        dy = mouse_pos[1] - prev_mouse_pos[1]
                        prev_mouse_pos = mouse_pos
                        # Adjust image position based on mouse movement
                        image_position_x += dx
                        image_position_y += dy
                else:
                    prev_mouse_pos = event.pos

            # Handle continuous image display when arrow key is pressed for a while
            if arrow_key_pressed:
                if pygame.time.get_ticks() - arrow_key_timer > arrow_key_delay:
                    # Check if the arrow key is still pressed for continuous scrolling
                    keys = pygame.key.get_pressed()
                    if arrow_key_pressed == pygame.K_RIGHT and keys[pygame.K_RIGHT]:
                        # Change the current image index for continuous scrolling
                        current_index_A = (current_index_A + 1) % len(images_A)
                        current_index_B = (current_index_B + 1) % len(images_B)
                    elif arrow_key_pressed == pygame.K_LEFT and keys[pygame.K_LEFT]:
                        current_index_A = (current_index_A - 1) % len(images_A)
                        current_index_B = (current_index_B - 1) % len(images_B)
                else:
                    # Change image once if the arrow key is pressed momentarily
                    if arrow_key_pressed == pygame.K_RIGHT:
                        current_index_A = (current_index_A + 1) % len(images_A)
                        current_index_B = (current_index_B + 1) % len(images_B)
                    elif arrow_key_pressed == pygame.K_LEFT:
                        current_index_A = (current_index_A - 1) % len(images_A)
                        current_index_B = (current_index_B - 1) % len(images_B)

    pygame.quit()




def draw_text(surface, text, font, color, position):
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, position)

# Get the directory of the current script
script_directory = os.path.dirname(os.path.abspath(__file__))

# Change the current working directory to the script directory
os.chdir(script_directory)

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

# Initialize running flag
running = True

# Load cases and display images
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
