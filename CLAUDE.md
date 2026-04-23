# multi_work Project

## Overview

This project uses a two-agent workflow to separate UI/design concerns from business logic:

- **design-agent** — responsible for all UI, layout, styling, and user-facing components
- **logic-agent** — responsible for data processing, API integration, state management, and business rules

## Agent Responsibilities

### design-agent
- Component markup and structure (HTML/JSX/templates)
- CSS, styling, and visual design
- Animations and transitions
- Responsive layout and accessibility
- Static assets and icons

### logic-agent
- Business logic and data transformations
- API calls and service integrations
- State management and data flow
- Validation and error handling
- Utilities and helpers

## Shared Conventions

- Components live in `src/components/`
- Business logic lives in `src/logic/`
- Shared types/interfaces live in `src/types/`
- Each agent must not modify files owned by the other agent without coordination

## Handoff Protocol

- design-agent exposes component props/interfaces in `src/types/`
- logic-agent implements the data contracts defined in `src/types/`
- Conflicts or overlapping concerns should be discussed before implementation

## Tech Stack

- HTML5 + CSS3 + Vanilla JavaScript (no build tools required)
- Static site: open `index.html` directly in a browser

## Project Structure

```
multi_work/
├── index.html          # main page (design-agent)
├── css/
│   └── style.css       # all styles (design-agent)
├── js/
│   └── app.js          # rendering + filtering logic (logic-agent)
└── data/
    └── news.json       # news data (logic-agent)
```

## DOM Interface Contract (shared between agents)

HTML elements that JS targets — design-agent must use these exact IDs/classes:

| ID / Class | Element | Purpose |
|---|---|---|
| `#category-filters` | div | container for filter buttons |
| `.filter-btn` + `data-category` attr | button | category filter button |
| `#search-input` | input | keyword search box |
| `#news-count` | span | displays "XX件" |
| `#news-grid` | div | card grid container |
| `#no-results` | div | empty state message |

News card markup (rendered by JS into `#news-grid`):
```html
<article class="news-card" data-category="{category-slug}">
  <div class="card-badge category-{category-slug}">{カテゴリ名}</div>
  <div class="card-body">
    <h2 class="card-title">{タイトル}</h2>
    <p class="card-summary">{概要}</p>
    <div class="card-footer">
      <time class="card-date">{日付}</time>
      <a class="card-link" href="{url}">続きを読む →</a>
    </div>
  </div>
</article>
```

## News Data Schema (news.json)

```json
{
  "id": "string",
  "title": "string",
  "category": "区政 | 防災 | イベント | 生活情報 | 子育て | 福祉",
  "categorySlug": "kusei | bousai | event | seikatsu | kosodate | fukushi",
  "date": "YYYY-MM-DD",
  "summary": "string (80文字以内)",
  "url": "string"
}
```
