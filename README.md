# Python Tkinter(ish) to Vanilla JS CSS Converter (WIP)

A web-based tool that converts Python 3 Tkinter GUI applications into standalone HTML/JavaScript web apps.

## Overview

This converter takes Python code using the Tkinter library and transforms it into a single HTML file with embedded CSS and vanilla JavaScript. The goal is to provide conceptual equivalents between Python/Tkinter and web technologies.

## What Is Supported

### Python Syntax Conversion

| Python | JavaScript |
|--------|------------|
| `def function_name():` | `function function_name() { }` |
| `lambda x: x + 1` | `(x) => x + 1` |
| `if condition:` / `else:` | `if (condition) { } else { }` |
| `str(value)` | `String(value)` |
| `global variable` | (handled automatically) |
| `root.after(ms, func)` | `setTimeout(func, ms)` |
| `variable = value` | `var variable = value;` |

### Tkinter Widgets → HTML Elements

| Tkinter Widget | HTML Output |
|----------------|-------------|
| `tk.Button` | `<button>` |
| `tk.Label` | `<span>` |
| `tk.Entry` | `<input type="text">` |
| `tk.Frame` | `<div class="frame-container">` |
| `tk.Checkbutton` | `<label><input type="checkbox">` |

### Widget Options

| Tkinter Option | HTML/CSS Output |
|----------------|-----------------|
| `text="Label"` | Inner text content |
| `bg="#RRGGBB"` | `style="background: #RRGGBB"` |
| `fg="#RRGGBB"` | `style="color: #RRGGBB"` |
| `width=N` | CSS width styling |
| `command=func` | `onclick` event handler |

### Layout Managers

| Tkinter | HTML/CSS |
|---------|----------|
| `.pack()` | Flexbox (column by default) |
| `side=tk.LEFT` | `flex-direction: row` + `float` or flex |
| `padx=N`, `pady=N` | CSS margin/padding |
| Nested Frames | Nested divs with flexbox |

### Event Handling

- **Button clicks**: `command=func` → `element.onclick = function() { func(); }`
- **Checkbutton toggle**: Uses `addEventListener("change", ...)` to detect checkbox state changes
- **StringVar**: Converted to checking `checkbox.checked` (boolean)

### Variable Types

| Python | JavaScript |
|--------|------------|
| `counter = 0` | `var counter = 0;` |
| `entry.get()` | `document.getElementById("wN").value` |
| `var.get()` (StringVar) | `document.querySelector("input[type=checkbox]").checked` |
| `label.config(text=...)` | `element.textContent = ...` |

## Usage

1. Open `converter.html` in a modern web browser
2. Enter your Python Tkinter code in the left panel
3. Click **Convert** to generate the HTML/JavaScript
4. Click **Download** to save the resulting HTML file
5. Open the downloaded HTML file in any browser

### Sample Code

The converter includes two sample programs:

- **Load Basic**: A simple counter with Start/Reset buttons
- **Load Full**: A comprehensive example with:
  - Counter with increment/decrement/reset
  - Text entry with submit
  - Checkbutton with toggle functionality
  - Timer functionality
  - Nested frames

## Limitations

- Complex nested if/else with elif not fully supported
- Class-based Tkinter applications require manual conversion
- Some advanced widget options not implemented
- Canvas widgets not supported
- Menu bars not supported
- Grid layout manager uses pack() approximation

## Technical Details

- **Output format**: Single HTML file with embedded `<style>` and `<script>` tags
- **No dependencies**: Pure vanilla JavaScript, no frameworks
- **Widget IDs**: Each widget gets a unique ID (`w0`, `w1`, etc.) for DOM manipulation
- **CSS**: Uses flexbox for layout, minimal styling included

## Example Conversion

### Python Input:
```python
import tkinter as tk

counter = 0

def increment():
    global counter
    counter = counter + 1
    label.config(text="Count: " + str(counter))
    if counter < 10:
        root.after(500, increment)

def on_reset():
    global counter
    counter = 0
    label.config(text="Count: 0")

root = tk.Tk()
root.title("Counter App")

label = tk.Label(root, text="Count: 0", bg="#eee")
label.pack()

btn1 = tk.Button(root, text="Start", command=increment, bg="#4CAF50", fg="white")
btn1.pack(side=tk.LEFT, padx=5)

btn2 = tk.Button(root, text="Reset", command=on_reset, bg="#f44336", fg="white")
btn2.pack(side=tk.LEFT, padx=5)

root.mainloop()
```

### JavaScript Output:
```html
<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>Counter App</title>
<style>
body{font-family:Arial;background:#f0f0f0;padding:20px}
#app{display:flex;flex-direction:column;align-items:center;gap:10px}
.frame-container{display:flex;flex-direction:row;align-items:center;gap:5px;margin:5px 0;padding:10px}
button{padding:10px 20px;cursor:pointer;border:1px solid #ccc;border-radius:4px;margin:0 5px}
span{display:inline-block;margin:5px 10px}
input{padding:8px;width:150px;border:1px solid #ccc;border-radius:4px;margin:5px 0}
label{cursor:pointer;margin:5px 10px;display:inline-flex;align-items:center;gap:5px}
#w1{background:#4CAF50}
#w2{background:#f44336}
</style></head><body>
<div id="app">
<span id="w0">Count: 0</span>
<button id="w1">Start</button>
<button id="w2">Reset</button>
</div>
<script>
var counter = 0;
function increment() {
    counter = counter + 1;
    document.getElementById("w0").textContent = "Count: " +String(counter);
    if (counter < 10) {
        setTimeout(increment, 500);
    }
}
function on_reset() {
    counter = 0;
    document.getElementById("w0").textContent = "Count: 0";
}

var el1 = document.getElementById("w1");
if (el1) { el1.onclick = function() { increment(); }; }
var el2 = document.getElementById("w2");
if (el2) { el2.onclick = function() { on_reset(); }; }

console.log("App loaded");
</script></body></html>
```

## License

MIT License
