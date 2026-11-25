# HACKER | Blue Team Integrity Monitor

[Português](#português) · [English](README.en.md)

## Português

Ferramenta offline em Python para criar uma linha de base SHA-256 e comparar arquivos adicionados, removidos e modificados em um diretório autorizado. Ela lê os arquivos, não altera os dados monitorados e não instala agente, serviço ou persistência.

### Reproduzir

Python 3.10 ou superior, sem dependências externas. Crie uma pasta `amostras` com arquivos de teste; mantenha o manifesto fora dela.

```bash
python integrity.py baseline amostras baseline.json
python integrity.py compare amostras baseline.json
python -m unittest discover -s tests -v
```

O primeiro comando recusa sobrescrever uma linha de base existente. Edite um arquivo de amostra e compare novamente. A saída lista somente caminhos relativos e o tipo de mudança, sem publicar o conteúdo dos arquivos.

### Códigos de saída

| Código | Significado |
| --- | --- |
| 0 | Linha de base criada ou comparação sem mudanças |
| 1 | Comparação detectou mudanças |
| 2 | Erro de entrada, acesso ou manifesto |

### Validação e limites

Os testes cobrem SHA-256, nomes relativos, inclusões/alterações/exclusões, diretório vazio/inexistente, códigos de saída e proteção do manifesto. A evidência da execução real está em `evidence/validacao.json`. O workflow repete os testes; consulte o resultado no Actions para confirmar execução remota.

O monitor não identifica se uma alteração é maliciosa. Uma atualização legítima também altera o hash. O manifesto deve ser criado de uma origem confiável e protegido separadamente: se ele for adulterado, o resultado perde valor. O programa não assina manifestos, não captura mudanças que ocorreram e foram revertidas entre varreduras e não garante uma fotografia atômica de arquivos em uso. Links simbólicos e pastas `.git` e `__pycache__` são ignorados. A ferramenta foi testada como exercício local; não equivale ao FIM do Wazuh ou a um produto de EDR.

### Investigação

Ao detectar mudança, consulte o responsável pelo ativo, o registro de mudança autorizado e a janela de manutenção; preserve as evidências e não faça rollback automático sem avaliar impacto. Este projeto não contém dados de empregadores.

Autor: Gabriel Christian de Oliveira. Preparado com apoio de IA; revisão em 25/11/2026. Commits atuais com prefixo `HACKER:`, sem alterar autoria ou datas antigas.
