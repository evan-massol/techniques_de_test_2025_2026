# Mon expérience de retour sur le TP de TDD

## Impressions Générales

Personnellement, l'utilisation d'une approche TDD pour la réalisation d'un projet n'est pas quelque chose que j'ai réellement aimé faire, notamment parce que j'avais l'impression d'être trop restreint dans ma façon de coder et dans ce que j'ai le droit ou non de faire. Toutefois, je peux comprendre les avantages de cette méthode, même si je ne pense pas la réutiliser à l'avenir.

Globalement, je pense avoir plutôt bien organisé les tests que j'ai réalisés, même s'il en manque peut-être quelques uns. J'ai essayé de couvrir les cas les plus importants et de m'assurer que chaque fonction était testée de manière adéquate. J'ai quand même eu du mal à anticiper tous les scénarios possibles, ce qui a conduit à des ajustements de code après coup (mais très peu sur les tests eux mêmes, et j'en suis assez content).

## Ce Qui a Bien Marché

### Organisation des Tests
- **Structure claire** : Séparation nette entre `unit_test.py` et `perf_test.py` a rendu la maintenance facile
- **Utilisation de `@pytest.mark.parametrize`** : Cela a permis de tester plusieurs cas avec un seul test, ce qui rend le code plus maintenable (j'ai découvert cette fonctionnalité pendant le TP et je l'ai trouvée très utile)
- **Utilisation du mocking** : Les mocks pour PointSetManager ont permis de tester l'API sans dépendre d'un service externe
- **Coverage élevé** : 90% de couverture de code sur 33 tests

### Processus TDD
- Le fait d'écrire les tests en premier a quand même clarifié les spécifications de l'API (structure binaire, codes d'erreur, etc.)
- Les tests ont servi à mieux comprendre ce que le code doit faire

## Ce Qui Aurait Pu Être Mieux

### Planification Initiale
- J'aurais aimé anticiper davantage certains aspects du projet avant de commencer à coder
- La gestion du format binaire aurait pu être mieux faite si j'avais planifié une classe dédiée pour ça je pense

### Algorithme de Triangulation
- J'aurais pu tester plus en profondeur l'algorithme de triangulation lui-même, notamment avec des cas limites (points colinéaires par exemple)


## Bilan

Le projet m'a surtout montré l'importance de :
- Bien comprendre les spécifications avant de coder
- Écrire des tests qui reflètent les cas réels
- Maintenir une bonne séparation des responsabilités
