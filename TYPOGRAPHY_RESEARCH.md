# Typography Capabilities Research - Tkhtml3/CSS 2.1

## Environment Context
- **Rendering Engine**: Tkhtml3 (via tkinterweb module)
- **CSS Support**: CSS 2.1 + some CSS3 extras
- **Font System**: Standard system fonts available in customtkinter
- **Current Font**: Segoe UI with fallback chain

## ✅ What WORKS in CSS 2.1

### Font Properties
```css
font-family: "Font Name", fallback, sans-serif;  /* Web-safe fonts */
font-weight: normal | bold | 700 (numeric 100-900); /* Varying weights */
font-style: normal | italic | oblique;
font-size: 12px | 1.5em | 120%;  /* Various units */
letter-spacing: 1px;  /* Kerning control */
line-height: 1.5;  /* Line spacing */
text-transform: uppercase | lowercase | capitalize;
text-decoration: underline | overline | line-through | none;
text-align: left | center | right | justify;
```

### Supported CSS 2.1 Features
- `border-radius` - rounded corners
- `linear-gradient` - background gradients
- `float` - text wrapping
- `position` - positioning (static, relative, absolute)
- `max-width` - content limiting
- `border` - various border styles (solid, dotted, dashed, etc.)
- `display: inline | block | inline-block`
- `:hover` - hover states (limited)
- `:nth-child()` - element selection

### Available Web-Safe Fonts
On Windows systems with modern browsers/renderers:
- **Serif**: Georgia, "Times New Roman", Times
- **Sans-serif**: "Segoe UI", "Helvetica Neue", Helvetica, Arial, Verdana, Tahoma
- **Monospace**: Monaco, "Courier New", Courier, "Courier"
- **Display**: Impact, "Arial Black"

## ❌ What DOES NOT WORK

- **Flexbox/Grid** - No modern layout
- **Box-shadow** - No text shadows
- **Transitions/Animations** - No motion effects
- **CSS Variables** - No var() custom properties
- **@media queries** - No responsive design built-in
- **Web fonts** - No @font-face or Google Fonts
- **SVG/filter effects** - Limited graphics
- **Transform** - No CSS transform property
- **Multiple text shadows** - No text-shadow at all
- **Complex pseudo-elements** - ::before, ::after limited

## 🎯 Practical Typography Strategies

### 1. Font Weight Variation (WORKS!)
```css
.title { font-weight: 700; }      /* Bold */
.subtitle { font-weight: 500; }   /* Medium - if supported */
.regular { font-weight: 400; }    /* Normal */
.light { font-weight: 300; }      /* Light - if supported */
```
**Numeric weights (300, 400, 500, 700, 900) work if font supports them**

### 2. Letter Spacing (WORKS!)
```css
.title { letter-spacing: 2px; }      /* Widely spaced */
.number { letter-spacing: -1px; }    /* Tightly spaced */
```

### 3. Text Transform (WORKS!)
```css
.uppercase { text-transform: uppercase; }
.small-caps { font-variant: small-caps; }  /* May work */
```

### 4. Font Size Hierarchy (WORKS!)
```css
h1 { font-size: 2.5em; }
h2 { font-size: 1.8em; }
h3 { font-size: 1.3em; }
.number { font-size: 3em; }
```

### 5. Borders & Decorative Lines (WORKS!)
```css
.item {
	border-left: 3px solid #color;     /* Left border */
	border-bottom: 1px solid #color;   /* Bottom border */
	border: none;                       /* Or no border */
}

/* Border styles: solid, dotted, dashed, double, groove, ridge, inset, outset */
border-bottom: 2px dotted #color;
border-left: 4px double #color;
```

### 6. Gradients (WORKS!)
```css
background: linear-gradient(90deg, #color1 0%, #color2 100%);
background: linear-gradient(180deg, rgba(255,255,255,0.1) 0%, transparent 100%);
```
**Note: Can use on text background, not directly on text**

### 7. Pseudo-elements (LIMITED)
```css
.item:hover { color: #highlight; }    /* Hover state works */
.item::before { content: "»"; }        /* May work but limited */
```

## 💡 Creative Typography Techniques

### Technique 1: Bold Initials/Numbers
```css
.number {
	font-weight: 700;
	font-size: 4em;
	letter-spacing: -2px;
	color: #4da6ff;
	font-family: "Segoe UI", sans-serif;
}
```

### Technique 2: Small Caps Effect
```css
.title {
	font-size: 1.2em;
	font-weight: 600;
	text-transform: uppercase;
	letter-spacing: 1.5px;
	font-variant: small-caps;
}
```

### Technique 3: Line-based Hierarchy
```css
.item {
	border-left: 3px solid #4da6ff;
	border-bottom: 1px solid #333;
	padding-left: 16px;
	padding-bottom: 20px;
}
```

### Technique 4: Multi-level Emphasis
```css
.primary { font-weight: 700; font-size: 1.1em; }  /* Main title */
.secondary { font-weight: 500; font-size: 1em; }  /* Subtitle */
.tertiary { font-weight: 400; font-size: 0.95em; } /* Details */
```

### Technique 5: Monospace for Contrast
```css
.number {
	font-family: "Courier New", monospace;
	font-weight: bold;
	letter-spacing: 3px;
}
```

## 🛠️ Recommended Approach for Title Page

Given constraints, here's what we CAN do:

1. **Large, Bold Numbers**: 4-5em, font-weight: 700, letter-spacing: -2px
2. **Weighted Titles**: 1.1-1.2em, font-weight: 600-700
3. **Borders**: Left border (3px solid color) + bottom border (1px solid #333)
4. **Spacing**: letter-spacing for numbers, line-height for readability
5. **Hover States**: Color change on :hover with smooth appearance
6. **Gradient Accents**: Background gradients for emphasis areas (if needed)

## Status Icons - Better Alternatives

Since checkmarks may not display well:
- **HTML entities**: `✓` (U+2713), `●` (U+25CF), `▪` (U+25AA), `▸` (U+25B8)
- **Unicode symbols**: Consider simpler alternatives
- **CSS-based**: Use border/background pseudo-elements to create shapes
- **Color coding**: Rely more on color than symbols

## Recommended Font Stack
```css
font-family: "Segoe UI", "Helvetica Neue", -apple-system, sans-serif;
```

This gives us:
- Modern look on Windows (Segoe UI)
- Fallback for Mac (Helvetica Neue)
- System font as last resort
- Clear, professional appearance

---

## Summary: Best Practices for Our Use Case

✅ **DO:**
- Use font-weight variations (300, 400, 600, 700)
- Use letter-spacing for emphasis (±1-2px)
- Use text-transform: uppercase for style
- Use borders for visual structure
- Use font-size hierarchy (3em for numbers, 1.1em for titles)
- Use color to indicate status

❌ **DON'T:**
- Expect text shadows or gradients on text itself
- Use @font-face or web fonts
- Expect animations or transitions
- Use flexbox or grid automatically
- Rely on complex pseudo-elements

---

This research shows we have plenty of room to make the title page look professional and polished using borders, weight, letter-spacing, and size variation!
