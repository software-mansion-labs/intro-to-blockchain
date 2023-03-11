### Instalacja
Skopiuj sobie to repozytorium komendą:
```
git clone https://github.com/software-mansion-labs/intro-to-blockchain.git
```

Do uczestnictwa w warsztatach potrzebujesz pythona 3, oraz dwie biblioteki które zainstalujesz poniższymi komendami:  

```
python3 -m venv venv
pip3 install -r requirements.txt
```

### Zadania

#### Zadanie 1
Do zaimplementowania masz metody w plikach:
- `hash_1.py`
- `public_key_2.py`
- `signature_3.py`

#### Zadanie 2
Do zaimplementowania masz metody w plikach:
- `transaction_registry.py`
- `wallet.py`

Dodatkowo, w pliku `playground.py` możesz w praktyce przetestować swoje rozwiązanie. Aby uruchomić "piaskownicę", wywołaj z **głównego** folderu repozytorium komendę `python3 -m exercise2.playground`

#### Zadanie 3
Do zaimplementowania masz metody w plikach:
- `block.py`
- `blockchain.py`
- `node.py`

### Jak testować rozwiązania?
Wywołaj `pytest` wewnątrz folderu danego zadania aby je przetestować.

### Masz problem z zadaniem?
W branchach `solution1`, `solution2` i `solution3` znajdują się rozwiązania odpowiednio pierwszego, drugiego i trzeciego zadania. Możesz je podejrzeć
lub lokalnie zmergować do mastera. W przypadku drugiej opcji najlepiej najpierw przywrócić stan folderu z ćwiczeniem do pierwotnego stanu aby uniknąć konfliktów, a następnie zmergować dany branch. Możesz to zrobić dwoma komendami:

```
git checkout -- exerciseX
git merge solutionX
```

podstawiając pod X numer zadania.
