"""
Prompts for Graphic Assets Generator Agent.
"""

GRAPHICS_SYSTEM_PROMPT = """You are an expert graphic designer and visual content strategist.
You specialize in creating specifications for social media graphics that are:
- Eye-catching and engaging
- On-brand and consistent
- Optimized for each platform's dimensions and best practices
- Designed to maximize engagement

Your role is to translate content and brand guidelines into detailed graphic design specifications."""

GRAPHIC_SPEC_PROMPT = """Based on the following information, create detailed graphic design specifications.

# Brand Information
Brand Name: {brand_name}
Brand Colors: {brand_colors}
Brand Fonts: {brand_fonts}
Brand Voice: {brand_voice}

# Content Information
Platform: {platform}
Content Type: {content_type}
Caption/Text: {caption}
Theme: {theme}

# Requirements
{requirements}

Create specifications for a graphic that includes:
1. **Dimensions**: Optimal size for the platform and content type
2. **Layout**: Composition and element placement
3. **Color Scheme**: Primary, secondary, and accent colors from brand palette
4. **Typography**: Font choices, sizes, and text hierarchy
5. **Visual Elements**: Images, icons, shapes, patterns to include
6. **Text Overlay**: Key text to display on the graphic
7. **Style Notes**: Overall aesthetic, mood, and style guidelines

Return as JSON:
{{
  "graphic_id": "unique-id",
  "platform": "{platform}",
  "content_type": "{content_type}",
  "dimensions": {{
    "width": 1080,
    "height": 1080,
    "unit": "px"
  }},
  "layout": {{
    "composition": "centered/split/grid/etc",
    "element_placement": "description of where elements go",
    "visual_hierarchy": "what should draw attention first"
  }},
  "color_scheme": {{
    "background": "#HEXCOLOR or gradient description",
    "primary": "#HEXCOLOR",
    "secondary": "#HEXCOLOR",
    "accent": "#HEXCOLOR"
  }},
  "typography": {{
    "headline": {{
      "text": "Main headline text",
      "font": "Font name",
      "size": "large/medium/small or specific px",
      "color": "#HEXCOLOR",
      "weight": "bold/normal/light"
    }},
    "subheadline": {{
      "text": "Subheadline text if any",
      "font": "Font name",
      "size": "medium/small",
      "color": "#HEXCOLOR"
    }},
    "body": {{
      "text": "Body text if any",
      "font": "Font name",
      "size": "small",
      "color": "#HEXCOLOR"
    }}
  }},
  "visual_elements": {{
    "background_style": "solid/gradient/image/pattern",
    "images": ["description of images to include"],
    "icons": ["list of icons needed"],
    "shapes": ["geometric shapes to use"],
    "patterns": "any patterns or textures"
  }},
  "style_notes": {{
    "aesthetic": "modern/minimalist/bold/playful/etc",
    "mood": "professional/energetic/calm/etc",
    "special_effects": "shadows, gradients, overlays, etc"
  }},
  "image_generation_prompt": "A detailed prompt for an AI image generator to create this graphic",
  "canva_template_suggestion": "Suggested Canva template type or search term"
}}
"""

BATCH_GRAPHICS_PROMPT = """Create graphic specifications for a batch of social media content.

# Brand Information
{brand_info}

# Content Batch
{content_batch}

For each piece of content, create a graphic specification optimized for its platform and type.
Maintain brand consistency across all graphics while varying layouts to keep content fresh.

Return as JSON array of graphic specifications following the same structure as single graphics.
"""

IMAGE_GEN_PROMPT_TEMPLATE = """Create a {style} social media graphic for {platform}.

Visual Content:
- {description}

Design Specifications:
- Dimensions: {dimensions}
- Color scheme: {colors}
- Typography: {typography}
- Style: {aesthetic}
- Mood: {mood}

The graphic should be {adjectives}, suitable for {brand_voice} brand targeting {target_audience}.

Include: {include_elements}
Exclude: {exclude_elements}

High quality, professional, social media ready."""
