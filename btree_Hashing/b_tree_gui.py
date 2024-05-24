import PySimpleGUI as sg
from b_tree import BTree
import time
from hash import HashTable

class DataStructureSelector:
    def __init__(self):
        sg.theme('SystemDefaultForReal')  # Setting a modern theme

        self.layout = [
            [sg.Image(filename='Media/universite.png', pad=(20, 0)), sg.Image(filename='Media/master.png', pad=(50, 0)), sg.Image(filename='Media/fstt.png', pad=(20, 0))],  
            [sg.Text('Select Data Structure', font=('Arial', 30, 'bold'), text_color='#333333', background_color='white', pad=(0, 80))],
            [sg.Radio('B-Tree', "RADIO1", font=('Arial', 18), default=True, text_color='#333333', background_color='white', key='b_tree_radio')],
            [sg.Radio('Hashing', "RADIO1", font=('Arial', 18), text_color='#333333', background_color='white', key='hashing_radio')],
            [sg.Button('Next', size=(10, 1), font=('Arial', 14), button_color=('white', '#0047ab'), border_width=0, pad=(0, 70))]
        ]
        self.window = sg.Window("Data Structure", self.layout, finalize=True, element_justification='center', size=(1000, 650), background_color='white')

    def run(self):
        while True:
            event, values = self.window.read()
            if event == sg.WINDOW_CLOSED:
                break
            elif event == 'Next':
                if values['b_tree_radio']:
                    self.window.close()
                    BTreeGUI().run()
                elif values['hashing_radio']:
                    self.window.close()
                    HashingGUI().run()
                break
        self.window.close()

class BTreeGUI:
    def __init__(self):
        self.b_tree = BTree(2)  # Initialize B-Tree with a default parameter
        self.node_width = 60
        self.node_height = 40
        self.layout = [
            [sg.Canvas(size=(1000, 500), background_color='white', key='canvas')],
            [sg.InputText("", key='input_insert', font=('Helvetica', 12)),
             sg.Button('Insert', font=('Open Sans', 12), button_color=('white', '#1B5E20'), size=(8, 1), pad=((5, 5), (5, 5))),
             sg.InputText("", key='input_delete', font=('Helvetica', 12)),
             sg.Button('Delete', font=('Open Sans', 12), button_color=('white', '#D32F2F'), size=(8, 1), pad=((5, 5), (5, 5)))],
            [sg.InputText("", key='input_search', font=('Helvetica', 12)),
             sg.Button('Search', font=('Open Sans', 12), button_color=('white', '#0D47A1'), size=(8, 1), pad=((5, 5), (5, 5))),
             sg.InputText("", key='input_update', font=('Helvetica', 12)),
             sg.Button('Update', font=('Open Sans', 12), button_color=('white', '#E65100'), size=(8, 1), pad=((5, 5), (5, 5)))],
            [sg.Button('Back', font=('Helvetica', 12), button_color=('#F0F0F0', '#14213D'), size=(8, 1), pad=(5, 20))]
        ]
        self.window = sg.Window("B Tree", self.layout, finalize=True)
        self.canvas = self.window['canvas'].TKCanvas
        self.canvas_x_center = 1000 / 2
        self.canvas_y_center = 500 / 2

    def run(self):
        self.draw_tree_step_by_step()
        while True:
            event, values = self.window.read()
            if event == sg.WINDOW_CLOSED or event == 'Back':
                break
            elif event == 'Insert':
                key = int(values['input_insert'])
                self.b_tree.insert(key)
                self.draw_tree_step_by_step()
            elif event == 'Delete':
                key = int(values['input_delete'])
                self.b_tree.delete(key)
                self.draw_tree_step_by_step()
            elif event == 'Search':
                key = int(values['input_search'])
                result = self.b_tree.search(key)
                if result:
                    sg.popup("Search Result", f"Value {key} found in the tree.")
                else:
                    sg.popup("Search Result", f"Value {key} not found in the tree.")
            elif event == 'Update':
                old_key_str = values['input_insert'].strip()
                new_key_str = values['input_update'].strip()

                if not old_key_str:
                    sg.popup("Update Error", "Please provide the old key.")
                    return

                old_key = int(old_key_str)

                # Check if the old key exists before updating
                if not self.b_tree.search(old_key):
                    sg.popup("Update Error", f"Value {old_key} does not exist in the tree.")
                    return

                if not new_key_str:
                    sg.popup("Update Error", "Please provide the new key.")
                    return

                new_key = int(new_key_str)
                self.update_key(old_key, new_key)
                self.draw_tree_step_by_step()

        self.window.close()
        if event == 'Back':
            DataStructureSelector().run()

    def draw_tree_step_by_step(self):
        self.canvas.delete("all")  # Clear the canvas
        self._draw_step_by_step_recursive(self.b_tree.root, self.canvas_x_center, 70, 200, 0, 0)
        time.sleep(1)  # Introduce a delay (adjust as needed)

    def _draw_step_by_step_recursive(self, node, x, y, spacing, parent_x, parent_y):
        if node:
            num_keys = len(node.keys)
            half_width = num_keys * spacing / 2

            for i, key in enumerate(node.keys):
                new_x = x - half_width + i * spacing

                if parent_x:
                    self.canvas.create_line(parent_x-30+ self.node_width / 2, parent_y + self.node_height / 2,
                                            new_x + self.node_width / 2, y, fill="black", width=2, dash=(4, 2))

                self.canvas.create_rectangle(new_x, y, new_x + self.node_width, y + self.node_height,
                                             outline="black", width=2)
                self.canvas.create_text(new_x + self.node_width / 2, y + self.node_height / 2, text=str(key),
                                        font='Helvetica 10 bold')

                if not node.leaf and i < len(node.children):
                    self._draw_step_by_step_recursive(node.children[i], new_x - 20 , y + 120, spacing/2 - 30,
                                                      new_x + self.node_width / 2, y + self.node_height / 2)

            if not node.leaf and len(node.children) > num_keys:
                self._draw_step_by_step_recursive(node.children[-1], new_x +30 + spacing, y + 120, spacing/2 + 10,
                                                    new_x + self.node_width / 2, y + self.node_height / 2)

    def update_key(self, old_key, new_key):
        # Check if the old key exists before updating
        if not self.b_tree.search(old_key):
            sg.popup("Update Error", f"Value {old_key} does not exist in the tree.")
            return

        self.b_tree.update(old_key, new_key)

class HashingGUI:
    def __init__(self):
        # Constants
        self.canvas_width = 1000
        self.canvas_height = 550
        self.table_size = 29
        self.hash_functions = {
            'Linear Probe': HashTable.add_element_linear_probe,
            'Double Hashing': HashTable.add_element_double_hashing,
            'Separate Chaining': HashTable.add_element_separate_chaining,
            'Internal Chaining': HashTable.add_element_internal_chaining
        }

        # GUI Components
        self.canvas = sg.Canvas(size=(self.canvas_width, self.canvas_height), background_color='white', key='canvas')
        input_elem = sg.Input(key='input_element', font=('Helvetica', 12), size=(10, 1))
        hash_type_elem = sg.Combo(['Linear Probe', 'Double Hashing', 'Separate Chaining', 'Internal Chaining'], 
                          key='combo_hash_type', 
                          font=('Helvetica', 10), 
                          size=(15, 1), 
                          background_color='#FFFFFF',  # White background
                          text_color='#333333',       # Dark gray text
                          readonly=False,              # Make it readonly
                          enable_events=True,         # Enable events
                          )
        add_button = sg.Button("Add to Hash Table", font=('Open Sans', 11), size=(14, 1), button_color=('white', '#1B5E20'))
        clear_button = sg.Button("Clear Hash Table", font=('Open Sans', 11), size=(14, 1), button_color=('white', '#D32F2F'))
        delete_button = sg.Button("Delete element", font=('Open Sans', 11), size=(14, 1), button_color=('white', '#E65100'))
        back_button = sg.Button('Back', font=('Helvetica', 12), button_color=('#F0F0F0', '#14213D'), size=(8, 1), pad=(5, 10))

        # Layout
        layout = [
            [self.canvas],
            [sg.Text("Enter Element:", font=('Roboto', 12)), input_elem, sg.Text("Select Hashing Type:", font=('Roboto', 12)), hash_type_elem, add_button, delete_button, clear_button],
            [back_button]
        ]

        # Window setup
        self.window = sg.Window("Hashing Visualization", layout, finalize=True, size=(1000, 650))
        self.hash_table = HashTable(self.table_size)

    def draw_hash_table(self):
        # Clear the canvas
        self.canvas.TKCanvas.delete("all")

        # Draw "Hash Table" text
        self.canvas.TKCanvas.create_text(self.canvas_width // 2, 30, text="Hash Table", anchor="n", font=("Helvetica", 20, "bold"))

        # Define cell dimensions and padding
        cell_width = 80
        cell_height = 25
        padding = 5

        # Draw hash table content
        for i in range(self.table_size):
            x = 320 if i < 15 else 80 + 450
            y = 70 + (i % 15) * (cell_height + padding) if i<15 else 70 + (i % 15) * (cell_height + padding) + 12

            # Draw index cell
            self.canvas.TKCanvas.create_rectangle(x, y, x + cell_width, y + cell_height, outline='black', fill='white')
            index_text = str(i)
            self.canvas.TKCanvas.create_text(x + cell_width // 2, y + cell_height // 2, text=index_text, anchor="center", font=("Helvetica", 14))

            # Draw element cell if an element exists
            if self.hash_table.table[i] is not None:
                element_text = str(self.hash_table.table[i])
                self.canvas.TKCanvas.create_rectangle(x + cell_width + padding, y, x + 2 * cell_width + padding, y + cell_height, outline='black', fill='#E0E0E0')
                self.canvas.TKCanvas.create_text(x + cell_width + padding + cell_width // 2, y + cell_height // 2, text=element_text, anchor="center", font=("Helvetica", 11))

    def clear_hash_table(self):
        self.hash_table = HashTable(self.table_size)
        self.draw_hash_table()

    def delete_from_hash_table(self, element):
        self.hash_table.delete_element(element)
        self.draw_hash_table()

    def add_to_hash_table(self, element, hash_type):
        if hash_type in self.hash_functions:
            self.hash_functions[hash_type](self.hash_table, element)
        else:
            sg.popup_error("Invalid hashing type selected.")
        self.draw_hash_table()

    def run(self):
        self.draw_hash_table()
        while True:
            event, values = self.window.read()
            if event == sg.WINDOW_CLOSED:
                break
            elif event == 'Add to Hash Table':
                element = values['input_element']
                hash_type = values['combo_hash_type']
                if element.isdigit():  
                    self.add_to_hash_table(element, hash_type)
                else:
                    sg.popup_error("Please enter a numerical element.")
            elif event == 'Clear Hash Table':
                self.clear_hash_table()
            elif event == 'Delete element':
                element = values['input_element']
                if element.isdigit():
                    self.delete_from_hash_table(element)
                else:
                    sg.popup_error("Please enter a numerical element.")
            elif event == 'Back':
                self.window.close()
                DataStructureSelector().run()

def main():
    DataStructureSelector().run()

if __name__ == "__main__":
    main()

