class Node:
    def __init__(self, name, is_dir=True, size=0, parent=None):
        self.name, self.is_dir, self.size, self.parent = name, is_dir, size, parent
        self.children = {} if is_dir else None

class FileSystem:
    def __init__(self):
        self.root = Node('/')
        self.current, self.used, self.max = self.root, 0, 1024
    
    def mkdir(self, name):
        if name in self.current.children: return f"Error: '{name}' exists"
        self.current.children[name] = Node(name, parent=self.current)
        return f"Directory '{name}' created"
    
    def cd(self, path):
        if path == '/': self.current = self.root
        elif path == '..' and self.current.parent: self.current = self.current.parent
        elif path in self.current.children and self.current.children[path].is_dir:
            self.current = self.current.children[path]
        else: return f"Error: '{path}' not found"
        return f"Changed to {self.pwd()}"
    
    def ls(self):
        return '\n'.join(f"{n}/" if c.is_dir else f"{n} ({c.size} KB)" 
                         for n, c in sorted(self.current.children.items()))
    
    def touch(self, name, size=10):
        if name in self.current.children: return f"Error: '{name}' exists"
        if self.used + size > self.max: return "Error: Quota exceeded"
        self.current.children[name] = Node(name, False, size, self.current)
        self.used += size
        return f"File '{name}' created ({size} KB)"
    
    def rm(self, name):
        if name not in self.current.children: return f"Error: '{name}' not found"
        freed = self._size(self.current.children[name])
        del self.current.children[name]
        self.used -= freed
        return f"'{name}' removed (freed {freed} KB)"
    
    def _size(self, n):
        return n.size if not n.is_dir else sum(self._size(c) for c in n.children.values())
    
    def pwd(self):
        path, node = [], self.current
        while node.parent: path.append(node.name); node = node.parent
        return '/' + '/'.join(reversed(path)) if path else '/'
    
    def quota(self):
        return f"{self.used}/{self.max} KB ({self.used*100/self.max:.1f}% used)"
    
    def tree(self, node=None, prefix=""):
        if node is None: node = self.current; print(self.pwd())
        for i, (name, child) in enumerate(sorted(node.children.items())):
            last = i == len(node.children) - 1
            print(f"{prefix}{'└── ' if last else '├── '}{name}{'/' if child.is_dir else f' ({child.size} KB)'}")
            if child.is_dir and child.children:
                self.tree(child, prefix + ('    ' if last else '│   '))

fs = FileSystem()
print("=" * 50 + "\n       FILE SYSTEM SIMULATOR\n" + "=" * 50)
print("Commands: mkdir, cd, ls, touch, rm, pwd, quota, tree, exit\n" + "=" * 50)

while True:
    try:
        cmd = input(f"\n{fs.pwd()} $ ").strip().split()
        if not cmd: continue
        
        if cmd[0] == 'exit': print("\nGoodbye!"); break
        elif cmd[0] == 'mkdir' and len(cmd) > 1: print(fs.mkdir(cmd[1]))
        elif cmd[0] == 'cd' and len(cmd) > 1: print(fs.cd(cmd[1]))
        elif cmd[0] == 'ls': output = fs.ls(); print(output) if output else None
        elif cmd[0] == 'touch' and len(cmd) > 1:
            print(fs.touch(cmd[1], int(cmd[2]) if len(cmd) > 2 else 10))
        elif cmd[0] == 'rm' and len(cmd) > 1: print(fs.rm(cmd[1]))
        elif cmd[0] == 'pwd': print(fs.pwd())
        elif cmd[0] == 'quota': print(fs.quota())
        elif cmd[0] == 'tree': fs.tree()
        else: print("Unknown command")
    except KeyboardInterrupt: print("\n\nGoodbye!"); break
    except: print("Error: Invalid command")
