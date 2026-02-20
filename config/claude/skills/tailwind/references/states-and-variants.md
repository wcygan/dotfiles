# Tailwind CSS — States & Variants

## Syntax

Every variant prefixes any utility: `{variant}:{utility}`

```html
hover:bg-blue-600      focus:ring-2         active:scale-95
dark:text-white        sm:flex-row          lg:hidden
disabled:opacity-50    required:border-red-500
```

Stack multiple variants: `dark:md:hover:bg-fuchsia-600`

---

## Pseudo-Class Variants

### Interactive States

```html
<button class="bg-blue-500 hover:bg-blue-600 focus:outline-2 active:bg-blue-700">
  Click me
</button>

<!-- focus-visible: only keyboard focus (not mouse click) -->
<button class="focus-visible:ring-2 focus-visible:ring-offset-2">

<!-- focus-within: element or any descendant is focused -->
<div class="focus-within:ring-2">
  <input type="text" />
</div>

<!-- visited link -->
<a class="text-blue-500 visited:text-purple-500">Link</a>
```

### Structural

```html
<!-- First/last/only child -->
<li class="py-4 first:pt-0 last:pb-0 border-b last:border-0">Item</li>

<!-- Odd/even (1-indexed) -->
<tr class="odd:bg-white even:bg-gray-50">

<!-- nth-child with arbitrary value -->
<li class="nth-[3n]:bg-yellow-100 nth-last-[2]:font-bold">

<!-- empty element -->
<p class="empty:hidden"><!-- nothing here --></p>
```

### Form States

```html
<!-- disabled -->
<input class="disabled:opacity-50 disabled:cursor-not-allowed" disabled />
<button class="enabled:hover:bg-blue-600" />

<!-- checked -->
<input type="checkbox" class="checked:bg-blue-500" />
<input type="checkbox" class="indeterminate:bg-gray-300" />

<!-- validation -->
<input class="invalid:border-red-500 invalid:text-red-600 focus:invalid:ring-red-500" />
<input class="valid:border-green-500" />
<input class="user-invalid:border-red-500" /> <!-- after user interaction -->

<!-- required/optional -->
<input class="required:border-orange-500" required />

<!-- in-range/out-of-range -->
<input type="number" min="1" max="10"
       class="in-range:border-green-500 out-of-range:border-red-500" />

<!-- placeholder-shown, autofill, read-only -->
<input class="placeholder-shown:border-gray-200 autofill:bg-yellow-50 read-only:text-gray-500" />
```

---

## Parent State (group)

Style children based on parent state:

```html
<a href="#" class="group block rounded-lg p-4 hover:bg-blue-500">
  <h3 class="text-gray-900 group-hover:text-white font-semibold">Title</h3>
  <p class="text-gray-500 group-hover:text-blue-100 text-sm">Description</p>
  <svg class="stroke-gray-400 group-hover:stroke-white h-5 w-5" />
</a>
```

### Named Groups (nested parents)

```html
<ul class="group/list">
  <li class="group/item flex items-center">
    <span class="text-gray-700 group-hover/item:text-blue-500">Item</span>
    <button class="opacity-0 group-hover/item:opacity-100 group-hover/list:opacity-50">
      Edit
    </button>
  </li>
</ul>
```

### Arbitrary Group (CSS class on parent)

```html
<div class="group is-published">
  <div class="hidden group-[.is-published]:block">Published badge</div>
</div>
```

### in-* (implicit parent, no group class needed)

```html
<div tabindex="0">
  <span class="opacity-50 in-focus:opacity-100">Content</span>
</div>
```

---

## Sibling State (peer)

Style elements based on a sibling's state:

```html
<form>
  <input id="email" type="email" class="peer border rounded px-3 py-2" />
  <p class="invisible peer-invalid:visible text-red-500 text-sm mt-1">
    Please enter a valid email.
  </p>
</form>
```

### Named Peers

```html
<input id="draft" class="peer/draft" type="radio" name="status" />
<label for="draft" class="peer-checked/draft:text-sky-500 peer-checked/draft:font-bold">
  Draft
</label>

<input id="pub" class="peer/pub" type="radio" name="status" />
<label for="pub" class="peer-checked/pub:text-green-500">Published</label>
```

---

## :has() Variant

Style a parent based on its descendants:

```html
<!-- Label gets indigo background when its radio is checked -->
<label class="has-checked:bg-indigo-50 has-checked:border-indigo-500 rounded-lg p-4 border">
  <input type="radio" class="checked:border-indigo-500" />
  <span class="text-gray-900">Google Pay</span>
</label>

<!-- Container when it has a link -->
<div class="group">
  <svg class="hidden group-has-[a]:block"><!-- icon --></svg>
  <p>Text <a href="#">with link</a></p>
</div>
```

---

## Negation (:not)

```html
<!-- Hover styles only when not focused -->
<button class="hover:not-focus:bg-indigo-700">Button</button>

<!-- Style all but the last -->
<li class="not-last:border-b">Item</li>
```

---

## ARIA Variants

```html
<!-- Boolean ARIA attributes -->
<div aria-checked="true" class="aria-checked:bg-sky-700">
<div aria-expanded="false" class="aria-expanded:rotate-180">  <!-- dropdown arrow -->
<div aria-disabled="true" class="aria-disabled:opacity-50">

<!-- All built-in: aria-busy, aria-checked, aria-disabled, aria-expanded,
                   aria-hidden, aria-pressed, aria-readonly, aria-required, aria-selected -->

<!-- Arbitrary ARIA values -->
<th aria-sort="ascending" class="aria-[sort=ascending]:bg-[url('/up.svg')]">
```

---

## Data Attribute Variants

```html
<!-- Boolean data attribute -->
<div data-active class="data-active:border-purple-500">

<!-- Value matching -->
<div data-size="large" class="data-[size=large]:p-8">
<div data-state="open" class="data-[state=open]:rotate-180">
```

---

## Pseudo-Element Variants

```html
<!-- before/after (add content-[''] or content-none) -->
<div class="before:content-[''] before:block before:h-px before:bg-gray-200">
<div class="after:content-['*'] after:text-red-500 after:ml-0.5">Required</div>

<!-- placeholder styling -->
<input class="placeholder:italic placeholder:text-gray-400" placeholder="Search..." />

<!-- File input button -->
<input type="file" class="file:mr-4 file:rounded-full file:border-0 file:bg-blue-50 file:px-4 file:py-2 file:text-sm file:font-semibold" />

<!-- List markers -->
<ul class="list-disc marker:text-blue-500">

<!-- Text selection -->
<p class="selection:bg-fuchsia-300 selection:text-fuchsia-900">Selectable text</p>
```

---

## Dark Mode

```html
<div class="bg-white dark:bg-gray-900 text-gray-900 dark:text-white">
  <p class="text-gray-600 dark:text-gray-300">Body text</p>
  <button class="bg-blue-500 hover:bg-blue-600 dark:bg-blue-600 dark:hover:bg-blue-700">
    Action
  </button>
</div>
```

Configure dark mode strategy in CSS:
```css
/* Default: media query */
@import "tailwindcss";

/* Selector-based (for JS-toggled dark mode) */
@custom-variant dark (&:where(.dark, .dark *));
```

---

## Open/Inert/RTL

```html
<!-- details/dialog open state -->
<details class="open:bg-gray-100 rounded-lg">
  <summary class="p-4 font-semibold">Details</summary>
  <div class="p-4">Content shown when open</div>
</details>

<!-- Inert sections -->
<fieldset inert class="inert:opacity-50 inert:cursor-not-allowed">

<!-- RTL/LTR directional styling -->
<div class="ltr:pl-3 rtl:pr-3">
<svg class="ltr:rotate-0 rtl:rotate-180">
```

---

## Custom Variants

```css
/* Simple selector variant */
@custom-variant theme-midnight (&:where([data-theme="midnight"] *));

/* Media query variant */
@custom-variant any-hover {
  @media (any-hover: hover) {
    &:hover { @slot; }
  }
}

/* Multi-condition */
@custom-variant hocus (&:hover, &:focus);
```

```html
<div data-theme="midnight">
  <button class="theme-midnight:bg-black theme-midnight:text-white">
    Midnight button
  </button>
</div>

<button class="any-hover:hover:bg-blue-500">
<button class="hocus:underline">
```
