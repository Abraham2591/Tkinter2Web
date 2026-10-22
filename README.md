# Tkinter2Web: Tkinter to HTML / CSS / JS converter

Paste Python 3 **tkinter** code into a single HTML file and get back a **self-contained, vanilla HTML + CSS + JavaScript page** that behaves like the original app. No build step, no dependencies, no server: `Tkinter2Web.html` is the whole project.

> **Status:** experimental. It translates a practical *subset* of Python and tkinter (see [Limitations](#limitations)). It has been checked by converting the bundled sample app and syntax-checking the output, not by an exhaustive test suite.

## How it works

1. **Transpiler** (in `Tkinter2Web.html`): a line- and indentation-aware Python-to-JavaScript translator. It handles classes, functions, control flow, f-strings, keyword arguments, lambdas and more.
2. **Tk runtime** (embedded in every generated page): a small vanilla-JS library that re-implements tkinter widgets, geometry managers, variables, events and `after` on top of the DOM and CSS flexbox/grid.
3. **Output**: one `.html` file containing the CSS, the runtime and your converted app. Copy it anywhere and open it in a browser.

## Usage

1. Open `Tkinter2Web.html` in a modern browser (Chrome, Edge, Firefox, Safari).
2. Paste tkinter code into the left pane (or click **Load sample**).
3. Use the **Preview** tab to run it, or the **HTML output** tab to inspect the generated page.
4. Click **Copy HTML** and save the result as `app.html`.

Lines the converter cannot translate are listed in a warning line under the tabs.

## Example

```python
import tkinter as tk

class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.n = tk.IntVar(value=0)
        self.pack()
        tk.Label(self, textvariable=self.n, font=("Arial", 20)).pack()
        tk.Button(self, text="+1", command=self.bump).pack()

    def bump(self):
        self.n.set(self.n.get() + 1)

root = tk.Tk()
root.title("Counter")
App(root)
root.mainloop()
```

becomes a standalone page with a working counter.

## What is supported

### Widgets
| Category | Widgets |
|---|---|
| Windows | `Tk`, `Toplevel` (title bar, `geometry`, `title`, `destroy`, menubar via `config(menu=...)`) |
| Containers | `Frame`, `LabelFrame`, `PanedWindow` (alias of `Frame`), `ttk.Notebook` (`add`, `select`) |
| Text & buttons | `Label` (text, `textvariable`, `image`), `Message`, `Button`, `Menubutton` (alias of `Button`), `Entry`, `Text`, `ScrolledText` |
| Choices | `Checkbutton`, `Radiobutton`, `Scale`, `Listbox`, `Spinbox`, `ttk.Combobox`, `OptionMenu` |
| Display | `Canvas`, `ttk.Progressbar`, `ttk.Separator`, `ttk.Treeview` (columns, headings, insert, delete, selection) |
| Menus | `Menu` with commands, separators and cascades, rendered as a dropdown menubar |
| Stubs / partial | `Scrollbar` (hidden, native scrolling used instead), `ttk.Style`, `PhotoImage`, `filedialog` (returns empty strings), `colorchooser` (uses a prompt) |

The `ttk.` and `tk.` prefixes are stripped, so `ttk.Button` and `tk.Button` map to the same widget.

### Layout
- **`pack`**: `side`, `fill`, `expand`, `anchor`, `padx`/`pady` (including `(left, right)` tuples), `ipadx`/`ipady`, built on flexbox.
- **`grid`**: `row`, `column`, `rowspan`, `columnspan`, `sticky`, padding, plus `columnconfigure` / `rowconfigure` weights, built on CSS grid.
- **`place`**: `x`, `y`, `relx`, `rely`, `width`, `height`, `relwidth`, `relheight`, `anchor`.
- Common options: `bg`/`fg`, `font` (tuple or string), `width`/`height` (characters or lines for text widgets), `padx`/`pady`, `bd`, `relief`, `cursor`, `anchor`, `justify`, `wraplength`, `state`, `command`, `textvariable`, `variable`, `values`, `from_`/`to`, `orient`.

### Variables, events and timers
- `StringVar`, `IntVar`, `DoubleVar`, `BooleanVar` with `get`, `set` and `trace_add`, kept in sync with widgets in both directions.
- `bind` / `bind_all` with `<Button-1/2/3>`, `<Double-Button-1>`, `<ButtonRelease>`, `<Motion>`, `<B1-Motion>`, `<Enter>`, `<Leave>`, `<MouseWheel>`, `<FocusIn/Out>`, `<Key>`, `<KeyPress>`, `<KeyRelease>`, named keys (`<Return>`, `<Escape>`, `<space>`, arrows), `<Control-x>` combos and virtual events such as `<<ListboxSelect>>`. The event object provides `x`, `y`, `x_root`, `y_root`, `keysym`, `char`, `keycode`, `delta`, `num` and `widget`.
- `after(ms, fn, *args)`, `after_idle`, `after_cancel` map to `setTimeout` / `clearTimeout`.

### Canvas
`create_rectangle`, `create_oval`, `create_line`, `create_text`, `create_polygon`, `delete` (id, tag or `"all"`), `move`, `coords`, `itemconfig`. Items are tracked in a display list and repainted with `requestAnimationFrame`.

### Dialogs
`messagebox` (`showinfo`, `showwarning`, `showerror`, `askyesno`, `askokcancel`, `askquestion`) and `simpledialog` (`askstring`, `askinteger`, `askfloat`) use the browser's native dialogs.

### HTTP: `requests`, `httpx`, `urllib`
- `requests.get/post/put/delete/patch/head/request` (also via `httpx`), with `params=`, `headers=`, `json=`, `data=` and `timeout=`.
- `urllib.request.urlopen` / `Request` and `urllib.parse.urlencode` / `quote` / `unquote`.
- Responses expose `.json()`, `.text`, `.content`, `.status_code`, `.ok`, `.headers` and `.raise_for_status()`.
- The browser cannot block on network calls, so any function that makes a request (or calls one that does) is converted to `async`, and the calls are `await`ed automatically.
- `.content` is exposed as an object URL so it works with the bundled PIL-style shims (`BytesIO`, `Image.open(...).resize(...)`, `ImageTk.PhotoImage`) and `Label(image=...)`.
- `threading.Thread(target=...).start()` runs the target as an async task (there are no real threads).

### Python language and standard library
- **Syntax**: `class` with inheritance (`tk.Frame`, `tk.Tk`, your own classes), `super().__init__`, `def` with defaults and `*args`, `if`/`elif`/`else`, `while`, `for ... in range(...)`, `for` over lists, dicts and `enumerate`, `try`/`except`/`finally`, `lambda`, conditional expressions, tuple unpacking, augmented assignment, `global`, one-line compound statements (`if x: return`), multi-line expressions.
- **Operators and literals**: `and`/`or`/`not`, `is`/`is not`, `in`/`not in`, `==`/`!=`, `//` on simple operands, `True`/`False`/`None`, f-strings (including `{x:.2f}` and `{n:02d}`), raw and triple-quoted strings.
- **Bound methods**: `command=self.method` is auto-bound to `this`.
- **Builtins**: `print` (to the console), `len`, `range`, `int`, `float`, `str`, `abs`, `min`, `max`, `sum`, `round`, `list`, `sorted`, `enumerate`.
- **Methods**: `.append`, `.upper`, `.lower`, `.strip`, `.split()`, `.startswith`, `.endswith`, dict `.items()` / `.keys()` / `.values()` / `.get(key, default)`.
- **Modules**: `math`, `random` (`random`, `randint`, `choice`, `uniform`), `time` (`time`, `strftime`), `datetime.now().strftime(...)`, `json` (`loads`, `dumps`).

## Limitations

- **No comprehensions**, slicing (`x[1:3]`), `%` formatting, `str.format`, `str.join`, `with` blocks, generators, decorators (dropped) or class-level attributes. The converter warns about these.
- Code after `root.mainloop()` runs immediately instead of after the window closes.
- `requests.Session()` and `httpx.Client()` are not supported.
- `widget["option"] = value` is converted to `config(...)` only when the variable was assigned from a widget constructor in the same file; reading `widget["option"]` is not supported.
- Pack layout with mixed `side` values in one container is approximate.
- Python integer/float semantics follow JavaScript (no big integers, `/` is always float division).
- Imports of other third-party modules are dropped, not emulated.
- Only plain function calls are awaited. A lambda that calls an async function gets no `await`.
- **Preview sandbox**: the live preview runs in a sandboxed iframe. Hosted environments that block outside network requests will make HTTP calls fail there. Copy the generated HTML to a local file to test network code.

## Project layout

```
Tkinter2Web.html   # the entire project: UI, transpiler, runtime and CSS
README.md
```

Inside `Tkinter2Web.html`:

| Block | Purpose |
|---|---|
| `<script type="text/plain" id="rt">` | Tk runtime (widgets, layout, events, HTTP shims), embedded verbatim into every output file |
| `<script type="text/plain" id="css">` | Styles for the generated window and widgets |
| `<script type="text/plain" id="sample">` | The bundled demo app |
| `convert(src)` | Python-to-JS transpiler |
| `build(js)` | Assembles the final standalone HTML document |

## Extending

- **Add a widget**: subclass `Misc` in the runtime (set `static _k`, implement `_mk()` and `_opt()`), then add its name to the `CLS` list in the transpiler so constructor calls get `new`.
- **Add a Python helper**: define a runtime function or object (for example `len` or `random`) and, if the syntax needs rewriting, add a regex in `ex()`.
- **Add a syntax rule**: statements are handled in `stmt()`, block headers in `head()`.

## Contributing

Issues and pull requests are welcome, especially failing tkinter snippets with the output you expected. Add a license file of your choice before publishing.
