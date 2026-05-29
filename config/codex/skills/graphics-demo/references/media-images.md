# Media, Images, And Layout Stability

## Description

Use this reference when styling images, figures, videos, thumbnails, avatars, hero media, or cards with media slots. The goal is to preserve meaning, reserve space, and avoid layout shift while keeping media responsive.

Browse current official docs before making precise claims about responsive images, `picture`, `srcset`, intrinsic dimensions, `object-fit`, aspect ratios, lazy loading, or alt text behavior.

## Docs To Browse

- MDN, Using images in HTML: https://developer.mozilla.org/en-US/docs/Web/Media/Guides/Images
- MDN, `<img>` element: https://developer.mozilla.org/en-US/docs/Web/HTML/Element/img
- MDN, Responsive images: https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Structuring_content/HTML_images#responsive_images
- MDN, `object-fit`: https://developer.mozilla.org/en-US/docs/Web/CSS/object-fit
- MDN, Understanding and setting aspect ratios: https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Box_sizing/Aspect_ratios

## Guidance

- Give meaningful images useful alt text. Use empty alt text only for decorative images.
- Reserve space with dimensions, `aspect-ratio`, or stable containers to prevent layout shift.
- Use `object-fit: cover` for cropped thumbnails and `object-fit: contain` when the whole image must remain visible.
- Use `figure` and `figcaption` when the caption is part of the content.
- Use `picture`, `srcset`, and `sizes` when art direction or density-sensitive media matters.
- Avoid dark, blurred, decorative media when the user needs to inspect the real object or state.

## Checks

- Does the page remain stable before media loads?
- Can the image be understood without seeing it when it is meaningful?
- Does cropping hide important content?
- Does the media slot keep the component layout stable when the image aspect ratio changes?
