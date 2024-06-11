import json

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Fabric.js JSON Rendering Example</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/fabric.js/5.3.0/fabric.min.js"></script>
    <style>
        body {{
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background-color: #f0f0f0;
        }}
        canvas {{
            border: 1px solid #ccc;
        }}
    </style>
</head>
<body>
    <canvas id="canvas" width="800" height="600"></canvas>
    <script>
        document.addEventListener('DOMContentLoaded', () => {{
        const canvas = new fabric.Canvas('canvas');

        // 示例 JSON 数据，可以从服务器获取或本地文件加载
        const json = {json_data}

        // 从 JSON 数据加载对象并渲染到画布
        canvas.loadFromJSON(json, canvas.renderAll.bind(canvas), function (o, object) {{
            console.log('Loaded object:', object);
        }});

        // 添加一些交互功能
        canvas.on('object:modified', function (e) {{
            console.log('Object modified:', e.target);
        }});

        canvas.on('object:added', function (e) {{
            console.log('Object added:', e.target);
        }});
    }});


    </script>
</body>
</html>
"""

# 示例 JSON 数据
data = {
    "version": "5.3.0",
    "objects": [
        {
            "type": "rect",
            "left": 100,
            "top": 100,
            "width": 200,
            "height": 100,
            "fill": "red",
            "angle": 45
        },
        {
            "type": "circle",
            "left": 400,
            "top": 200,
            "radius": 50,
            "fill": "green"
        },
        {
            "type": "text",
            "left": 200,
            "top": 300,
            "text": "Hello, Fabric.js!",
            "fontSize": 30,
            "fill": "blue"
        }
    ]
}

def render_html(json_str):
    # 替换占位符
    html_result = html_template.format(json_data=json_str)

    # 输出或保存 HTML
    with open('output.html', 'w') as file:
        file.write(html_result)

    print("HTML generated successfully.")
