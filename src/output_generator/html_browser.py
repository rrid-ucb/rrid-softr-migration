"""
Generate a self-contained HTML browser for output directory.

Creates a single-page application that allows browsing all video runs
without requiring a web server.
"""

import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class HTMLBrowserGenerator:
    """Generate self-contained HTML browser for output directory."""
    
    def __init__(self, output_dir: Path):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def scan_outputs(self) -> Dict:
        """Scan output directory and build structure."""
        structure = {
            "videos": {},
            "total_runs": 0,
            "latest_run": None
        }
        
        if not self.output_dir.exists():
            return structure
        
        latest_timestamp = None
        
        for video_dir in self.output_dir.iterdir():
            if not video_dir.is_dir() or video_dir.name.startswith('.'):
                continue
            
            video_name = video_dir.name
            video_info = {
                "name": video_name,
                "runs": [],
                "latest_run": None
            }
            
            # Scan runs
            for run_dir in sorted(video_dir.iterdir(), reverse=True):
                if not run_dir.is_dir() or not run_dir.name.replace('_', '').isdigit():
                    continue
                
                run_timestamp = run_dir.name
                run_info = self._scan_run(run_dir, video_name)
                
                if run_info:
                    video_info["runs"].append(run_info)
                    structure["total_runs"] += 1
                    
                    # Track latest
                    if latest_timestamp is None or run_timestamp > latest_timestamp:
                        latest_timestamp = run_timestamp
                        structure["latest_run"] = {
                            "video": video_name,
                            "run": run_timestamp,
                            "path": f"{video_name}/{run_timestamp}"
                        }
                    
                    if video_info["latest_run"] is None or run_timestamp > video_info["latest_run"]["timestamp"]:
                        video_info["latest_run"] = {
                            "timestamp": run_timestamp,
                            "path": f"{video_name}/{run_timestamp}"
                        }
            
            if video_info["runs"]:
                structure["videos"][video_name] = video_info
        
        return structure
    
    def _scan_run(self, run_dir: Path, video_name: str) -> Optional[Dict]:
        """Scan a single run directory."""
        run_timestamp = run_dir.name
        
        # Load metadata if available
        metadata_path = run_dir / "run_metadata.json"
        metadata = {}
        if metadata_path.exists():
            try:
                with open(metadata_path) as f:
                    metadata = json.load(f)
            except Exception:
                pass
        
        run_info = {
            "timestamp": run_timestamp,
            "path": f"{video_name}/{run_timestamp}",
            "metadata": metadata,
            "frames": {"count": 0, "path": None},
            "transcripts": {"files": []},
            "docs": {}
        }
        
        # Scan frames
        frames_dir = run_dir / "frames"
        if frames_dir.exists():
            frames = list(frames_dir.glob("*.jpg"))
            if frames:
                run_info["frames"] = {
                    "count": len(frames),
                    "path": f"{run_info['path']}/frames"
                }
        
        # Scan transcripts
        transcripts_dir = run_dir / "transcripts"
        if transcripts_dir.exists():
            transcripts = []
            for transcript_file in transcripts_dir.glob("*.json"):
                transcripts.append({
                    "name": transcript_file.name,
                    "path": f"{run_info['path']}/transcripts/{transcript_file.name}"
                })
            for transcript_file in transcripts_dir.glob("*.md"):
                transcripts.append({
                    "name": transcript_file.name,
                    "path": f"{run_info['path']}/transcripts/{transcript_file.name}"
                })
            run_info["transcripts"]["files"] = transcripts
        
        # Scan docs
        docs_dir = run_dir / "docs"
        if docs_dir.exists():
            for model_dir in docs_dir.iterdir():
                if not model_dir.is_dir():
                    continue
                
                model_name = model_dir.name
                docs = []
                for doc_file in model_dir.glob("*.md"):
                    docs.append({
                        "name": doc_file.stem,
                        "filename": doc_file.name,
                        "path": f"{run_info['path']}/docs/{model_name}/{doc_file.name}"
                    })
                
                if docs:
                    run_info["docs"][model_name] = docs
        
        # Only return if run has content
        if run_info["frames"]["count"] > 0 or run_info["transcripts"]["files"] or run_info["docs"]:
            return run_info
        
        return None
    
    def generate_html_browser(self) -> Path:
        """Generate self-contained HTML browser."""
        structure = self.scan_outputs()
        
        # Generate HTML
        html_content = self._generate_html(structure)
        
        # Save to output directory
        index_path = self.output_dir / "index.html"
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        return index_path
    
    def _generate_html(self, structure: Dict) -> str:
        """Generate the HTML content."""
        structure_json = json.dumps(structure, indent=2)
        
        # Use regular string (not f-string) to avoid conflicts with JS template literals
        html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Video Annotation Output Browser</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: #f5f5f5;
            color: #333;
            line-height: 1.6;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        .header h1 {{
            font-size: 2rem;
            margin-bottom: 0.5rem;
        }}
        
        .header p {{
            opacity: 0.9;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 2rem;
        }}
        
        .sidebar {{
            background: white;
            border-radius: 8px;
            padding: 1.5rem;
            margin-bottom: 2rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        .sidebar h2 {{
            font-size: 1.25rem;
            margin-bottom: 1rem;
            color: #667eea;
        }}
        
        .video-list {{
            list-style: none;
        }}
        
        .video-item {{
            margin-bottom: 1rem;
        }}
        
        .video-name {{
            font-weight: 600;
            color: #333;
            margin-bottom: 0.5rem;
            cursor: pointer;
            padding: 0.5rem;
            border-radius: 4px;
            transition: background 0.2s;
        }}
        
        .video-name:hover {{
            background: #f0f0f0;
        }}
        
        .video-name.active {{
            background: #667eea;
            color: white;
        }}
        
        .run-list {{
            list-style: none;
            margin-left: 1rem;
            margin-top: 0.5rem;
        }}
        
        .run-item {{
            margin-bottom: 0.5rem;
        }}
        
        .run-link {{
            color: #667eea;
            text-decoration: none;
            padding: 0.25rem 0.5rem;
            border-radius: 4px;
            display: inline-block;
            transition: background 0.2s;
            font-size: 0.9rem;
        }}
        
        .run-link:hover {{
            background: #f0f0f0;
        }}
        
        .run-link.active {{
            background: #667eea;
            color: white;
        }}
        
        .run-link.latest {{
            font-weight: 600;
        }}
        
        .content {{
            background: white;
            border-radius: 8px;
            padding: 2rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            min-height: 400px;
        }}
        
        .run-header {{
            border-bottom: 2px solid #667eea;
            padding-bottom: 1rem;
            margin-bottom: 2rem;
        }}
        
        .run-header h2 {{
            color: #667eea;
            margin-bottom: 0.5rem;
        }}
        
        .run-meta {{
            color: #666;
            font-size: 0.9rem;
        }}
        
        .section {{
            margin-bottom: 2rem;
        }}
        
        .section h3 {{
            color: #333;
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 1px solid #eee;
        }}
        
        .doc-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 1rem;
        }}
        
        .doc-card {{
            border: 1px solid #ddd;
            border-radius: 6px;
            padding: 1rem;
            transition: transform 0.2s, box-shadow 0.2s;
            cursor: pointer;
        }}
        
        .doc-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }}
        
        .doc-card h4 {{
            color: #667eea;
            margin-bottom: 0.5rem;
        }}
        
        .doc-card .model-badge {{
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 0.25rem 0.5rem;
            border-radius: 4px;
            font-size: 0.75rem;
            margin-top: 0.5rem;
        }}
        
        .doc-viewer {{
            margin-top: 2rem;
            padding: 1.5rem;
            background: #f9f9f9;
            border-radius: 6px;
            max-height: 600px;
            overflow-y: auto;
        }}
        
        .doc-viewer h4 {{
            margin-bottom: 1rem;
            color: #667eea;
        }}
        
        .markdown-content {{
            line-height: 1.8;
        }}
        
        .markdown-content h1, .markdown-content h2, .markdown-content h3 {{
            margin-top: 1.5rem;
            margin-bottom: 1rem;
            color: #333;
        }}
        
        .markdown-content img {{
            max-width: 100%;
            height: auto;
            border-radius: 4px;
            margin: 1rem 0;
        }}
        
        .markdown-content code {{
            background: #f4f4f4;
            padding: 0.2rem 0.4rem;
            border-radius: 3px;
            font-family: 'Monaco', 'Courier New', monospace;
            font-size: 0.9em;
        }}
        
        .markdown-content pre {{
            background: #f4f4f4;
            padding: 1rem;
            border-radius: 4px;
            overflow-x: auto;
            margin: 1rem 0;
        }}
        
        .markdown-content pre code {{
            background: none;
            padding: 0;
        }}
        
        .loading {{
            text-align: center;
            padding: 2rem;
            color: #666;
        }}
        
        .empty-state {{
            text-align: center;
            padding: 3rem;
            color: #999;
        }}
        
        @media (min-width: 768px) {{
            .layout {{
                display: grid;
                grid-template-columns: 300px 1fr;
                gap: 2rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <div class="container">
            <h1>📹 Video Annotation Output Browser</h1>
            <p>Browse all video processing runs and generated documentation</p>
        </div>
    </div>
    
    <div class="container">
        <div class="layout">
            <div class="sidebar">
                <h2>Videos & Runs</h2>
                <ul class="video-list" id="videoList"></ul>
            </div>
            
            <div class="content" id="content">
                <div class="empty-state">
                    <p>Select a run from the sidebar to view details</p>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        const structure = {STRUCTURE_JSON_PLACEHOLDER};
        
        let currentRun = null;
        let currentDoc = null;
        
        function init() {{
            renderSidebar();
            if (structure.latest_run) {{
                loadRun(structure.latest_run.video, structure.latest_run.run);
            }}
        }}
        
        function renderSidebar() {{
            const videoList = document.getElementById('videoList');
            videoList.innerHTML = '';
            
            for (const [videoName, videoInfo] of Object.entries(structure.videos)) {{
                const videoItem = document.createElement('li');
                videoItem.className = 'video-item';
                
                const videoNameEl = document.createElement('div');
                videoNameEl.className = 'video-name';
                videoNameEl.textContent = videoName;
                videoNameEl.onclick = () => {{
                    if (videoInfo.latest_run) {{
                        loadRun(videoName, videoInfo.latest_run.timestamp);
                    }}
                }};
                
                const runList = document.createElement('ul');
                runList.className = 'run-list';
                
                for (const run of videoInfo.runs) {{
                    const runItem = document.createElement('li');
                    runItem.className = 'run-item';
                    
                    const runLink = document.createElement('a');
                    runLink.className = 'run-link';
                    if (run.timestamp === videoInfo.latest_run?.timestamp) {{
                        runLink.className += ' latest';
                    }}
                    runLink.textContent = formatTimestamp(run.timestamp);
                    runLink.href = '#';
                    runLink.onclick = (e) => {{
                        e.preventDefault();
                        loadRun(videoName, run.timestamp);
                    }};
                    
                    runItem.appendChild(runLink);
                    runList.appendChild(runItem);
                }}
                
                videoItem.appendChild(videoNameEl);
                videoItem.appendChild(runList);
                videoList.appendChild(videoItem);
            }}
        }}
        
        function formatTimestamp(timestamp) {{
            // Format YYYYMMDD_HHMMSS to readable date
            const year = timestamp.substring(0, 4);
            const month = timestamp.substring(4, 6);
            const day = timestamp.substring(6, 8);
            const hour = timestamp.substring(9, 11);
            const minute = timestamp.substring(11, 13);
            return `${{year}}-${{month}}-${{day}} ${{hour}}:${{minute}}`;
        }}
        
        async function loadRun(videoName, runTimestamp) {{
            currentRun = {{video: videoName, timestamp: runTimestamp}};
            currentDoc = null;
            
            const runInfo = structure.videos[videoName]?.runs.find(r => r.timestamp === runTimestamp);
            if (!runInfo) return;
            
            const content = document.getElementById('content');
            content.innerHTML = `
                <div class="run-header">
                    <h2>${{videoName}} - Run ${{formatTimestamp(runTimestamp)}}</h2>
                    <div class="run-meta">
                        ${{runInfo.frames.count}} frames • 
                        ${{runInfo.transcripts.files.length}} transcripts • 
                        ${{Object.keys(runInfo.docs).length}} model variants
                    </div>
                </div>
                
                <div class="section">
                    <h3>📄 Documentation</h3>
                    <div class="doc-grid" id="docGrid"></div>
                </div>
                
                <div class="section">
                    <h3>🎬 Frames</h3>
                    <p>Frames: ${{runInfo.frames.count}}</p>
                </div>
                
                <div class="section">
                    <h3>📝 Transcripts</h3>
                    <p>Transcript files: ${{runInfo.transcripts.files.length}}</p>
                </div>
                
                <div id="docViewer"></div>
            `;
            
            renderDocs(runInfo.docs);
            updateActiveLinks(videoName, runTimestamp);
        }}
        
        function renderDocs(docs) {{
            const docGrid = document.getElementById('docGrid');
            docGrid.innerHTML = '';
            
            for (const [modelName, docList] of Object.entries(docs)) {{
                for (const doc of docList) {{
                    const docCard = document.createElement('div');
                    docCard.className = 'doc-card';
                    docCard.onclick = () => loadDoc(doc.path, doc.name, modelName);
                    
                    docCard.innerHTML = `
                        <h4>${{doc.name}}</h4>
                        <span class="model-badge">${{modelName}}</span>
                    `;
                    
                    docGrid.appendChild(docCard);
                }}
            }}
        }}
        
        async function loadDoc(docPath, docName, modelName) {{
            currentDoc = {{path: docPath, name: docName, model: modelName}};
            
            const docViewer = document.getElementById('docViewer');
            docViewer.innerHTML = '<div class="loading">Loading document...</div>';
            
            try {{
                // Load markdown file
                const response = await fetch(docPath);
                if (!response.ok) {{
                    throw new Error('Failed to load document');
                }}
                
                const markdown = await response.text();
                const html = markdownToHtml(markdown, docPath);
                
                docViewer.innerHTML = `
                    <div class="doc-viewer">
                        <h4>${{docName}} <span class="model-badge">${{modelName}}</span></h4>
                        <div class="markdown-content">${{html}}</div>
                    </div>
                `;
            }} catch (error) {{
                docViewer.innerHTML = `
                    <div class="doc-viewer">
                        <p style="color: red;">Error loading document: ${{error.message}}</p>
                        <p>Path: ${{docPath}}</p>
                    </div>
                `;
            }}
        }}
        
        function markdownToHtml(markdown, basePath) {{
            // Simple markdown to HTML converter
            let html = markdown;
            
            // Headers
            html = html.replace(/^### (.*$)/gim, '<h3>$1</h3>');
            html = html.replace(/^## (.*$)/gim, '<h2>$1</h2>');
            html = html.replace(/^# (.*$)/gim, '<h1>$1</h1>');
            
            // Bold
            html = html.replace(/\\*\\*(.*?)\\*\\*/g, '<strong>$1</strong>');
            
            // Italic (but not if it's part of bold)
            html = html.replace(/(?<!\\*)\\*(?!\\*)([^*]+)\\*(?!\\*)/g, '<em>$1</em>');
            
            // Code blocks
            html = html.replace(/```([\\\\s\\\\S]*?)```/g, '<pre><code>$1</code></pre>');
            html = html.replace(/`([^`]+)`/g, '<code>$1</code>');
            
            // Images - fix relative paths
            html = html.replace(/!\\\\[([^\\\\]]*)\\\\]\\\\(([^)]+)\\)/g, (match, alt, src) => {{
                // Convert relative paths to absolute from output root
                if (src.startsWith('../')) {{
                    // Count ../ to determine depth
                    const depth = (src.match(/\\.\\.\\//g) || []).length;
                    const parts = basePath.split('/');
                    const newPath = parts.slice(0, -depth - 1).join('/') + '/' + src.replace(/\\.\\.\\//g, '');
                    return `<img src="${{newPath}}" alt="${{alt}}" />`;
                }}
                return `<img src="${{src}}" alt="${{alt}}" />`;
            }});
            
            // Links
            html = html.replace(/\\\\[([^\\\\]]+)\\\\]\\\\(([^)]+)\\)/g, '<a href="$2">$1</a>');
            
            // Lists
            html = html.replace(/^\\* (.+)$/gim, '<li>$1</li>');
            html = html.replace(/(<li>.*<\\/li>)/s, '<ul>$1</ul>');
            
            // Paragraphs
            html = html.split('\\\\n\\\\n').map(p => {{
                if (p.trim() && !p.match(/^<[h|u|o|l|d]/)) {{
                    return `<p>${{p.trim()}}</p>`;
                }}
                return p;
            }}).join('\\\\n');
            
            return html;
        }}
        
        function updateActiveLinks(videoName, runTimestamp) {{
            // Update active states
            document.querySelectorAll('.video-name').forEach(el => {{
                el.classList.remove('active');
            }});
            document.querySelectorAll('.run-link').forEach(el => {{
                el.classList.remove('active');
            }});
        }}
        
        // Initialize on load
        init();
    </script>
</body>
</html>
"""
        
        # Replace placeholder with actual JSON
        html_content = html_template.replace("{STRUCTURE_JSON_PLACEHOLDER}", structure_json)
        return html_content

