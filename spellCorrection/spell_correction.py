import re
from spellchecker import SpellChecker
import hunspell
import language_tool_python
from difflib import SequenceMatcher
from rich.console import Console
from rich.text import Text

console = Console()


def highlight_differences(prepend_msg, false_phrase, correct_phrase, style_ok="green", style_ko="bold red"):
    # Supprimer les espaces pour la comparaison
    false_phrase_no_spaces = false_phrase.replace(" ,", ",")
    correct_phrase_no_spaces = correct_phrase.replace(" ,", ",")

    matcher = SequenceMatcher(None, false_phrase_no_spaces, correct_phrase_no_spaces)
    highlighted_text = Text()
    highlighted_text.append(prepend_msg , style="white")

    # Comparaison caractère par caractère
    i_false = 0
    i_correct = 0
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        false_chunk = false_phrase_no_spaces[i1:i2]
        correct_chunk = correct_phrase_no_spaces[j1:j2]

        if tag == 'equal':
            # Partie correcte (vert)
            highlighted_text.append(false_chunk, style=style_ok)
        elif tag == 'replace':
            # Partie incorrecte remplacée (rouge gras)
            highlighted_text.append(false_chunk, style=style_ko)
        elif tag == 'delete':
            # Partie supprimée (rouge gras)
            highlighted_text.append(false_chunk, style=style_ko)
        elif tag == 'insert':
            # Partie ajoutée (on la saute dans la phrase incorrecte)
            pass

        # Met à jour les index dans les phrases d'origine
        i_false += len(false_chunk)
        i_correct += len(correct_chunk)

    return highlighted_text

def compare_phrases(false_phrase, correct_phrase):
    matcher = SequenceMatcher(None, false_phrase, correct_phrase)
    differences = []
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag != 'equal':
            differences.append({
                'operation': tag,
                'false_text': false_phrase[i1:i2],
                'correct_text': correct_phrase[j1:j2]
            })
    return differences


def corriger_orthographe_01(texte):
    """
  Corrige les fautes d'orthographe dans un texte en français avec spellchecker.

  Args:
    texte: Le texte à corriger.

  Returns:
    Le texte corrigé.
  """
    # Initialiser le correcteur orthographique spellchecker
    spell = SpellChecker(language='fr')

    # Séparer les mots et la ponctuation
    mots = re.findall(r'\w+|[^\w\s]', texte, re.UNICODE)

    # Corriger chaque mot
    mots_corriges = []
    for mot in mots:
      # Vérifier si le mot est mal orthographié
      if mot not in spell:
        # Obtenir la correction
        correction = spell.correction(mot)
        mots_corriges.append(correction)
      else:
        mots_corriges.append(mot)

    # Reconstituer le texte
    phrase_corrige = ' '.join(mots_corriges).replace(" ,", ",")
    phrase_corrige = phrase_corrige.replace(" ' ", "'")
    return phrase_corrige


def corriger_orthographe_02(texte):
  """
  Corrige les fautes d'orthographe dans un texte en français avec hunspell.

  Args:
      texte: Le texte à corriger.

  Returns:
      Le texte corrigé.
  """
  # Initialize the Hunspell spell checker for French
  spell = hunspell.HunSpell('/usr/share/hunspell/fr.dic', '/usr/share/hunspell/fr.aff')

  mots = texte.split()
  mots_corriges = []
  for mot in mots:
    if not spell.spell(mot):
      suggestions = spell.suggest(mot)
      if suggestions:
        mots_corriges.append(suggestions[0])
      else:
        mots_corriges.append(mot)
    else:
      mots_corriges.append(mot)
  return ' '.join(mots_corriges)


def corriger_orthographe_03(texte):
  """
  Corrige les fautes d'orthographe dans un texte en français avec language_tool_python.

  Args:
      texte: Le texte à corriger.

  Returns:
      Le texte corrigé.
  """
  # Initialize the LanguageTool spell checker for French
  spell = language_tool_python.LanguageTool('fr-FR')
  matches = spell.check(texte)
  texte_corrige = language_tool_python.utils.correct(texte, matches)
  return texte_corrige


if __name__ == '__main__':

    # Exemple d'utilisation
    texte_faux = "Voici un exenple de texte, de l'auteur François Martin, avic moins de 24 fotes d'ortographe."
    texte_correct = "Voici un exemple de texte, de l'auteur François Martin, avec moins de 24 fautes d'orthographe."
    console.print(highlight_differences("Texte faux :\t",texte_faux, texte_correct, style_ok="white"))
    texte_corrige_01 = corriger_orthographe_01(texte_faux)
    console.print(highlight_differences("spellchecker :\t",texte_corrige_01, texte_correct))
    # different_words = compare_phrases(texte_faux, texte_corrige_01)
    # for diff in different_words:
    #   print(f"Opération : {diff['operation']}")
    #   print(f"Texte incorrect : {diff['false_text']}")
    #   print(f"Texte correct : {diff['correct_text']}")
    #   print(diff)

    texte_corrige_02 = corriger_orthographe_02(texte_faux)
    console.print(highlight_differences(" hunspell    :\t", texte_corrige_02, texte_correct))
    texte_corrige_03 = corriger_orthographe_03(texte_faux)
    console.print(highlight_differences("LanguageTool :\t", texte_corrige_03, texte_correct))
