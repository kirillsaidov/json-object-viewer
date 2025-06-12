# module main

# system
import os
import json
from datetime import datetime

# web
import aiofiles
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

from .schemas import *

# app
app = FastAPI()
fdir = os.path.dirname(__file__) # pwd

# mount the files directory to serve static files
files_path = os.path.join(fdir, '..', 'files')
if not os.path.exists(files_path): os.mkdir(files_path)
app.mount('/files', StaticFiles(directory=files_path), name='files')


@app.get('/favicon.ico')
def favicon():
    return FileResponse(os.path.join(fdir, '..', 'imgs', 'favicon.ico'))


@app.get('/', response_class=HTMLResponse)
async def serve_html():
    async with aiofiles.open(os.path.join(fdir, 'templates', 'index.html'), mode='r') as f:
        html_content = await f.read()
    return HTMLResponse(content=html_content)


@app.get('/check-graph-exists')
async def check_graph_exists(file_name: str = Query(...)):
    if not file_name.endswith('.graph.json'): file_name += '.graph.json'
    file_path = os.path.join(fdir, '..', 'files', file_name)
    return {'exists': os.path.exists(file_path)}


@app.post('/save-graph')
async def save_graph(payload: SaveGraphRequest):
    # unpack
    file_name = payload.file_name
    graph_data = payload.graph_data
    
    # validate the file name
    if not file_name.endswith('.graph.json'): file_name += '.graph.json'
    file_path = os.path.join(fdir, '..', 'files', file_name)
    
    # write the file
    try:
        with open(file_path, 'w') as f:
            json.dump(graph_data, f, indent=4)
        return {'status': 'success', 'message': f'File {file_name} saved successfully'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get('/list-graphs')
async def list_graphs():
    files_dir = os.path.join(fdir, '..', 'files')
    if not os.path.exists(files_dir):
        os.makedirs(files_dir, exist_ok=True)
    
    graph_files = []
    for file in os.listdir(files_dir):
        if file.endswith('.graph.json'):
            file_path = os.path.join(files_dir, file)
            # get file size and modification time
            stat = os.stat(file_path)
            graph_files.append({
                'name': file,
                'size': stat.st_size,
                'mod_time': stat.st_mtime,
                'mod_time_readable': datetime.fromtimestamp(stat.st_mtime).strftime('%d-%m-%Y, %H:%M:%S'),
            })
    
    # sort by modification time (newest first)
    graph_files.sort(key=lambda x: x['mod_time'], reverse=True)
    return graph_files


@app.delete('/delete-graph/{file_name}')
async def delete_graph(file_name: str):
    # security: ensure we only allow deleting .graph.json files
    if not file_name.endswith('.graph.json') or '..' in file_name or '/' in file_name or '\\' in file_name:
        raise HTTPException(status_code=400, detail='Invalid file name')
    
    file_path = os.path.join(fdir, '..', 'files', file_name)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail='File not found')
    
    try:
        os.remove(file_path)
        return {'status': 'success', 'message': f'File {file_name} deleted'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
