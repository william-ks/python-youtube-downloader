# Youtube Downloader

![downloads](https://img.shields.io/github/downloads/atom/atom/total.svg)
![build](https://img.shields.io/appveyor/ci/:user/:repo.svg)
![chat](https://img.shields.io/discord/:serverId.svg)

## Table of Contents

- [Dependencies](#dependencies)
- [Description](#description)
- [Usage](#usage)
- [Photos](#photos)

## Dependencies

- Python: [Download Python 3.12.1](https://www.python.org/ftp/python/3.12.1/python-3.12.1-amd64.exe)
- Virtual Environment (pyvenv): Run the following command in the terminal:
```bash
    pip install virtualenv
```

## Usage
1. Clone the application repository:

```bash
git clone <repository-url> downloaderApp
```
2. Navigate to the downloaded folder using the terminal.
```bash
cd  ./downloaderApp
```

3. Create a virtual environment:

```bash
python -m venv venv
```
if this step generate a error go to [Error-Handling](#error-handling)

4. Activate the virtual environment:

### On Windows:
```bash
.\venv\Scripts\activate
```
### On Linux/Mac:
```bash
source venv/bin/activate
```
5. Install the project dependencies:

```bash
pip install -r requirements.txt
```
6. Run the application:

```bash
python main.py
```

7. Follow app steps

## Photos

1.![first Step](image.png)
2.![Alt text](image-1.png)
3.![image](https://hackmd.io/_uploads/HydXAUU9p.png)
4.![image](https://hackmd.io/_uploads/BkEQXD89p.png)
5.![image](https://hackmd.io/_uploads/Hk6WXvI5a.png)
6.![image](https://hackmd.io/_uploads/HkaSmD85T.png)
## Error-Handling

### Authorization Error ( Windows )
![image](https://hackmd.io/_uploads/BkHGeP856.png)
Para correção, em um terminal como admin faça o seguinte comando
```bash
Set-ExecutionPolicy Unrestricted
```