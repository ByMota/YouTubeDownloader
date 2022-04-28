import PySimpleGUI as sg
from pytube import YouTube

def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%d:%02d:%02d" % (hour, minutes, seconds)

def progress_check(stream, chunk, bytes_remaining):
    window['DOWNLOADPROGRESS'].update(100 - round(bytes_remaining / stream.filesize * 100))

def on_complete(stream, file_path):
    window['DOWNLOADPROGRESS'].update(0)

sg.theme("Default1")

start_layout = [[sg.InputText(key = 'INPUT'),sg.Button("Confirmar")]]


info_tab = [[sg.Text('Titulo:'),sg.Text('',key = 'TITLE')],
    [sg.Text('Tamanho:'),sg.Text('', key = 'LENGTH')],
    [sg.Text('Views:'),sg.Text('', key = 'VIEWS')],
    [sg.Text('Autor:'),sg.Text('', key = 'AUTHOR')],
    [sg.Text('Descrição:'),sg.Multiline('', key = 'DESCRIPTION',
    size = (40,20),no_scrollbar = False, disabled = True)]]

download_tab = [ [sg.Frame('Melhor Qualidade',[[sg.Button('Download', key = 'BEST'),sg.Text('',key = 'BESTRES'),sg.Text('',key = 'BESTSIZE')]])],
    [sg.Frame('Pior Qualidade',[[sg.Button('Download', key = 'WORST'),sg.Text('',key = 'WORSTRES'),sg.Text('',key = 'WORSTSIZE')]])],
    [sg.Frame('Audio',[[sg.Button('Download', key = 'AUDIO'),sg.Text('',key = 'AUDIOSIZE')]])],
    [sg.VPush()],
    [sg.Progress(100,orientation='h', size=(20, 20), key='DOWNLOADPROGRESS', expand_x = True)]]

layout = [[sg.TabGroup([[
    sg.Tab("Info", info_tab), sg.Tab("Download", download_tab)]])]]

window = sg.Window("YouTube Downloader", start_layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    if event == "Confirmar":
        video = YouTube(values["INPUT"], on_progress_callback = progress_check, on_complete_callback = on_complete)
        window.close()

        #Video Info
        window = sg.Window("YouTube Downloader", layout, finalize = True)
        window["TITLE"].update(video.title)
        window["LENGTH"].update(convert(video.length))
        window["VIEWS"].update(video.views)
        window["AUTHOR"].update(video.author)
        window["DESCRIPTION"].update(video.description)

        #Video Download
        window['BESTSIZE'].update(f'{round(video.streams.get_highest_resolution().filesize / 1048576,1)} MB')
        window['BESTRES'].update(video.streams.get_highest_resolution().resolution)        

        window['WORSTSIZE'].update(f'{round(video.streams.get_lowest_resolution().filesize / 1048576,1)} MB')
        window['WORSTRES'].update(video.streams.get_lowest_resolution().resolution)

        window['AUDIOSIZE'].update(f'{round(video.streams.get_audio_only().filesize / 1048576,1)} MB')
    
    if event == "BEST":
        video.streams.get_highest_resolution().download()

    if event == "WORST":
        video.streams.get_lowest_resolution().download()

    if event == "AUDIO":
        video.streams.get_audio_only().download()

window.close()

