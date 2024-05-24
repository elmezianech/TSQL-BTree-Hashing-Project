import PySimpleGUI as sg

class BTreeNode:
    def __init__(self, leaf=True):
        self.leaf = leaf
        self.keys = []
        self.children = []

class BTree:
    def __init__(self, t):
        self.root = BTreeNode()
        self.t = t

    def insert(self, key):
        root = self.root
        if len(root.keys) == (2 * self.t) - 1:
            new_root = BTreeNode(leaf=False)
            new_root.children.append(self.root)
            self.split(new_root, 0)
            self.root = new_root
        if not self._insert_non_full(self.root, key):
            sg.popup("Insertion Error", f"Key {key} already exists in the tree.")

    def _insert_non_full(self, x, key):
        i = len(x.keys) - 1
        if x.leaf:
            while i >= 0 and key < x.keys[i]:
                i -= 1
            if i >= 0 and key == x.keys[i]:
                return False  # Key already exists, return False
            x.keys.insert(i + 1, key)
            return True
        else:
            while i >= 0 and key < x.keys[i]:
                i -= 1
            i += 1
            if len(x.children[i].keys) == (2 * self.t) - 1:
                self.split(x, i)
                if key > x.keys[i]:
                    i += 1
            return self._insert_non_full(x.children[i], key)

    def split(self, x, i):
        t = self.t
        y = x.children[i]
        z = BTreeNode(leaf=y.leaf)
        x.children.insert(i + 1, z)
        x.keys.insert(i, y.keys[t - 1])
        z.keys = y.keys[t:2 * t - 1]
        y.keys = y.keys[0:t - 1]

        if not y.leaf:
            z.children = y.children[t:2 * t]
            y.children = y.children[0:t] 

    def search(self, key, x=None):
        if x is None:
            x = self.root
        i = 0
        while i < len(x.keys) and key > x.keys[i]:
            i += 1
        if i < len(x.keys) and key == x.keys[i]:
            return True
        elif x.leaf:
            return False
        else:
            return self.search(key, x.children[i])

    def delete(self, key):
        self._delete(self.root, key)

    def _delete(self, x, key):
        t = self.t
        i = 0
        while i < len(x.keys) and key > x.keys[i]:
            i += 1

        if x.leaf:
            if i < len(x.keys) and key == x.keys[i]:
                x.keys.pop(i)
            else:
                sg.popup("Erreur", "La clé {} n'est pas présente dans l'arbre.".format(key))
        else:
            if i < len(x.keys) and key == x.keys[i]:
                # The key to delete is in an internal node
                self.delete_internal_node(x, i)
            else:
                # The key to delete is not in this node; recurse to the appropriate child
                self._delete_nonempty_node(x, i, key)

            # After deletion, if the root has no keys and has one child, update the root
            if x == self.root and not x.keys and len(x.children) == 1:
                self.root = x.children[0]

    def delete_internal_node(self, x, i):
        t = self.t
        key = x.keys[i]
        if len(x.children[i].keys) >= t:
            predecessor = self.get_predecessor(x, i)
            x.keys[i] = predecessor
            self._delete(x.children[i], predecessor)
        elif len(x.children[i + 1].keys) >= t:
            successor = self.get_successor(x, i)
            x.keys[i] = successor
            self._delete(x.children[i + 1], successor)
        else:
            self.merge(x, i)
            self._delete(x.children[i], key)

    def _delete_nonempty_node(self, x, i, key):
        t = self.t
        if len(x.children[i].keys) == t - 1:
            if i > 0 and len(x.children[i - 1].keys) >= t:
                self.borrow_from_left(x, i)
            elif i < len(x.children) - 1 and len(x.children[i + 1].keys) >= t:
                self.borrow_from_right(x, i)
            elif i > 0:
                self.merge(x, i - 1)
            else:
                self.merge(x, i)

        self._delete(x.children[i], key)

    def borrow_from_left(self, x, i):
        child = x.children[i]
        sibling = x.children[i - 1]
        child.keys.insert(0, x.keys[i - 1])
        x.keys[i - 1] = sibling.keys.pop()

        if not child.leaf:
            child.children.insert(0, sibling.children.pop())

    def borrow_from_right(self, x, i):
        child = x.children[i]
        sibling = x.children[i + 1]
        child.keys.append(x.keys[i])
        x.keys[i] = sibling.keys.pop(0)

        if not child.leaf:
            child.children.append(sibling.children.pop(0))

    def merge(self, x, i):
        t = self.t
        child = x.children[i]
        sibling = x.children[i + 1]
        child.keys.append(x.keys[i])
        child.keys.extend(sibling.keys)
        x.keys.pop(i)
        x.children.pop(i + 1)

        if not child.leaf:
            child.children.extend(sibling.children)

    def is_node_full(self, node):
        return len(node.keys) == (2 * self.t) - 1

    def update(self, old_key, new_key):
        # Check if the old key exists before updating
        if not self.search(old_key):
            sg.popup("Update Error", f"Key {old_key} does not exist in the tree.")
            return

        # First, delete the old key
        self.delete(old_key)

        # Then, insert the new key
        self.insert(new_key)

    def get_successor(self, x, i):
        """
        Get the successor of a key in a node.
        """
        current_node = x.children[i + 1]
        while not current_node.leaf:
            current_node = current_node.children[0]
        return current_node.keys[0]