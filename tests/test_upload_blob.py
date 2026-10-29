import base64
import io
from types import SimpleNamespace

from PIL import Image

from app.core.config import Configuracoes
from app.services.upload_service import ServicoUpload


def _imagem_base64() -> str:
    buffer = io.BytesIO()
    Image.new("RGB", (20, 20), (200, 30, 30)).save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()


def test_url_postgres_e_normalizada():
    cfg = Configuracoes(DATABASE_URL="postgres://u:p@host/db?sslmode=require")
    assert cfg.database_url.startswith("postgresql://")


def test_upload_produto_usa_blob_quando_token_existe(monkeypatch):
    enviados = []

    def falso_put(caminho, dados, **kwargs):
        enviados.append(caminho)
        return SimpleNamespace(url=f"https://loja.public.blob.vercel-storage.com/{caminho}")

    monkeypatch.setenv("BLOB_READ_WRITE_TOKEN", "token-de-teste")
    monkeypatch.setattr("vercel.blob.put", falso_put)
    monkeypatch.setattr("vercel.blob.list_objects", lambda **kwargs: SimpleNamespace(blobs=[]))

    sucesso, erro, url = ServicoUpload().salvar_foto_produto("abc", _imagem_base64())

    assert sucesso, erro
    assert url.startswith("https://loja.public.blob.vercel-storage.com/produtos/abc/")
    assert enviados == ["produtos/abc/foto_0.jpg"]


def test_upload_perfil_blob_retorna_base_absoluta(monkeypatch):
    monkeypatch.setenv("BLOB_READ_WRITE_TOKEN", "token-de-teste")
    monkeypatch.setattr(
        "vercel.blob.put",
        lambda caminho, dados, **kw: SimpleNamespace(url=f"https://loja.public.blob.vercel-storage.com/{caminho}"),
    )
    monkeypatch.setattr("vercel.blob.list_objects", lambda **kwargs: SimpleNamespace(blobs=[]))

    servico = ServicoUpload()
    sucesso, erro, urls = servico.salvar_foto_perfil("u1", _imagem_base64())

    assert sucesso, erro
    base = servico.url_base_perfil("u1", urls)
    assert base.startswith("https://loja.public.blob.vercel-storage.com/perfis/u1/")
    assert urls["thumb"] == f"{base}/thumb.jpg"
