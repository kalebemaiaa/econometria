# Econometria

Para o primeiro trabalho de econometria desenvolvi um arquivo para replicar algumas funções da [biblioteca PNADcIBGE, feita para R](https://github.com/cran/PNADcIBGE), a principal necessidade é baixar os dados do PNADc para determinado trimestre de um ano. Para tanto, foi usado como um exemplo a [biblioteca Python pnadium](https://github.com/ggximenez/pnadium) para as funcionalidades específicas (como sample da amostra total e utilização do sas file para interpretar melhor as columas).

Como pré requisitos para instalar e rodar o projeto, é necessário ter instalado o [Python](https://www.python.org/downloads/), para executar os scripts, e o [Git](https://git-scm.com/downloads) para clonar o repositório.

## Instalação

Comece clonando e navegando para o repositório utilizando
```bash
git clone https://github.com/kalebemaiaa/econometria.git
cd econometria
```

(**OPCIONALMENTE**) Crie uma venv (exemplo para windows podem ser encontrados [aqui](https://docs.python.org/pt-br/3.13/library/venv.html)):
```bash
python3 -m venv venv
source venv/bin/activate
```

Finalmente, instale todas as depêndencias:
```bash
pip install -r requirements.txt
```

## Usage

Após instalado, o arquivo essêncial para ser utilizado é o [pnadcibge](./pnadcibge.py), ele possui algumas funções para baixar e extrair os arquivos PNAD do IBGE.

1. Comece fazendo o download dos dados de determinado ano/trimestre utilizando a função [download_data](./pnadcibge.py#24) que retorna um dicionario com os caminhos dos dados baixados:
```python
dict_paths = pnadcibge.download_data(year=2019, trimestre=3)
```

2. De posse dos caminhos, utilize a função [extract_data](./pnadcibge.py#66) que também retorna um dicionáio, dessa vez indicando os arquivos extraídos:
```python
dict_paths = pnadcibge.extract_data(paths = dict_paths)
```

3. Utilizando os caminhos dos arquivos extraídos, finalmente é possível gerar o dataframe utilizando a função [create_dataframe](./pnadcibge.py#127):
```python
df = pnadcibge.create_dataframe(dict_paths, 
                               columns_intrested=None, 
                               sample_size=0.1, 
                               random_seed=42)
```
Note que nesse caso, todos argumentos tirando **dict_paths** são opcionais, entretanto, utilizar columns_intrested e sample_size ajuda a reduzir o peso computacional de extrair e trabalhar com estes dados.

4. (**OPCIONALMENTE**) É altamente recomendável exportar o dataframe final para algum formato de interesse (.csv, .parquet, .xlsx, ...), visto que os arquivos baixados são excluídos após a execução de cada função: 
```python
df.to_csv("/caminho/para/arquivo.csv")
```

5. A partir desse momento, basta apenas manipular as informações. Algumas outras formas de utilizar é concatenar dados de determinado ano extraindo ele por trimestre.

## Links úteis

[Parquet file format](https://parquet.apache.org/)
[O que é PNADc](https://www.ibge.gov.br/estatisticas/sociais/trabalho/9171-pesquisa-nacional-por-amostra-de-domicilios-continua-mensal.html?=&t=o-que-e)
[read_fwf do pandas](https://pandas.pydata.org/docs/reference/api/pandas.read_fwf.html)