# dayekang.info — static site for GitHub Pages

Wix 사이트(dayekang.info)의 콘텐츠를 그대로 옮긴 정적 사이트입니다.
프레임워크 없이 순수 HTML/CSS라서 GitHub Pages에 바로 올릴 수 있습니다.

## 구성

| 파일 | 내용 |
|---|---|
| `index.html` | About (bio + News) |
| `publications.html` | 논문 8편 (썸네일·초록·PDF/DOI 링크) |
| `data-science.html` | Book Recommendation, Color Palette 카드 |
| `ux-research.html` | Lexia, Nudge, My Little Hero, Sunshine, Tomorrow 카드 |
| `artwork.html` | 아트워크 갤러리 (25점, masonry) |
| `teaching.html` | Teaching 탭 (빈 틀 — 추후 채우기) |
| 프로젝트 상세 7개 | bookrecommendation, color, lexiainwonderland, nudgedesign, mylittlehero, sunshine, tomorrow |
| `style.css` | 공용 스타일 |
| `build.py` | 페이지 생성 스크립트 (수정 후 `python3 build.py`로 재생성) |
| `localize_images.py` | 이미지 로컬화 스크립트 (아래 참고) |

## GitHub Pages에 올리기

1. GitHub에서 새 repo 생성 — 이름은 반드시 `<내계정>.github.io`
2. 이 폴더의 파일 전부를 repo에 push:
   ```bash
   cd 이_폴더
   git init && git add -A && git commit -m "Personal website"
   git branch -M main
   git remote add origin https://github.com/<내계정>/<내계정>.github.io.git
   git push -u origin main
   ```
3. 몇 분 뒤 `https://<내계정>.github.io` 에서 확인
   (repo Settings → Pages 에서 Source가 `main` branch인지 확인)

## ⚠️ 이미지 로컬화 (중요)

지금 이미지들은 Wix 서버(`static.wixstatic.com`) 원본 URL을 그대로 참조합니다.
당장은 잘 보이지만 **Wix 구독을 해지하면 이미지가 깨질 수 있습니다.**

인터넷 되는 내 컴퓨터에서 한 번만 실행:
```bash
python3 localize_images.py
```
→ 모든 이미지를 `assets/` 폴더로 다운로드하고 HTML을 로컬 경로로 자동 수정합니다.
그 후 git commit & push 하면 완전히 독립된 사이트가 됩니다.

CV PDF와 논문 PDF들(`dayekang.info/_files/...`)도 Wix에 있으니,
해지 전에 `assets/`에 옮기고 링크를 바꿔주세요.

## 커스텀 도메인 (dayekang.info) 연결 — 나중에

1. repo에 `CNAME` 파일 생성, 내용은 한 줄: `www.dayekang.info`
2. 도메인 등록업체 DNS에서:
   - `www` CNAME → `<내계정>.github.io`
   - apex(@) A 레코드 → 185.199.108.153 / 109.153 / 110.153 / 111.153
3. repo Settings → Pages → Custom domain에 도메인 입력, Enforce HTTPS 체크
