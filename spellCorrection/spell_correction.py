import re

from nltk.translate.bleu_score import modified_precision
from spellchecker import SpellChecker
import hunspell
import language_tool_python
from difflib import SequenceMatcher
from rich.console import Console
from rich.text import Text




def highlight_differences(prepend_msg, original, modified, style_ok="green", style_replace="bold red", style_insert="bold magenta", style_delete="bold strike yellow"):
    # Supprimer les espaces pour la comparaison
    original_no_spaces = original.replace(" ,", ",")
    modified_no_spaces = modified.replace(" ,", ",")

    matcher = SequenceMatcher(None, original_no_spaces, modified_no_spaces)
    highlighted_text = Text()
    highlighted_text.append(prepend_msg , style="white")


    # Comparaison caractère par caractère
    i_false = 0
    i_correct = 0
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        original_chunk = original_no_spaces[i1:i2]
        modified_chunk = modified_no_spaces[j1:j2]

        if tag == 'equal':
            # Partie correcte (vert)
            highlighted_text.append(original_chunk, style=style_ok)
        elif tag == 'replace':
            # Partie incorrecte remplacée (rouge gras)
            highlighted_text.append(modified_chunk, style=style_replace)
        elif tag == 'delete':
            # Partie supprimée (rouge gras)
            highlighted_text.append(original_chunk, style=style_delete)
        elif tag == 'insert':
            # Partie ajoutée (on la saute dans la phrase incorrecte)
            highlighted_text.append(modified_chunk, style=style_insert)

        # Met à jour les index dans les phrases d'origine
        i_false += len(original_chunk)
        i_correct += len(modified_chunk)


    return highlighted_text


def count_differences(original, modified):
    matcher = SequenceMatcher(None, original, modified)
    count_equal = 0
    count_replace = 0
    count_insert = 0
    count_delete = 0
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        original_chunk = original[i1:i2]
        modified_chunk = modified[j1:j2]
        if tag == 'equal':
            count_equal += len(original_chunk)
        elif tag == 'replace':
            count_replace += len(original_chunk)
        elif tag == 'insert':
            count_insert += len(modified_chunk)
        elif tag == 'delete':
            count_delete += len(original_chunk)
        else:
            raise ValueError(f"Opération inconnue : {tag}")

    return { 'equal': count_equal, 'replace': count_replace, 'insert': count_insert, 'delete': count_delete }


def get_highlighted_differences_counter(prepend_msg, original_phrase, modified_phrase, style_ok="green", style_replace="bold red", style_insert="bold magenta", style_delete="bold yellow"):
    counters=count_differences(original_phrase, modified_phrase)
    highlighted_text = Text()
    highlighted_text.append(prepend_msg, style="white")
    highlighted_text.append(f"equal : {counters['equal']}, ", style=style_ok)
    highlighted_text.append(f"replace : {counters['replace']}, ", style=style_replace)
    highlighted_text.append(f"insert : {counters['insert']}, ", style=style_insert)
    highlighted_text.append(f"delete : {counters['delete']}", style=style_delete)
    return highlighted_text


def compare_phrases(original, modified):
    matcher = SequenceMatcher(None, original, modified)
    differences = []
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        #if tag != 'equal':
        differences.append({
            'operation': tag,
            'original_text': original[i1:i2],
            'modified_text': modified[j1:j2],
            'original_start': i1,
            'original_end': i2,
            'modified_start': j1,
            'modified_end': j2
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
  # https://pypi.org/project/language-tool-python/
  # Initialize the LanguageTool spell checker for French
  with language_tool_python.LanguageTool('fr-FR') as tool:
      matches = tool.check(texte)
      texte_corrige = language_tool_python.utils.correct(texte, matches)
      return texte_corrige


if __name__ == '__main__':
    import sys

    console = Console()
    GoDEBUG = False
    # check number of arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "-d":
            GoDEBUG = True

        if sys.argv[1] == "-h":
            print("Usage: python3 spell_correction.py [-d] [-h] \"texte à corriger\" ")
            print("Options:")
            print("\t-d\tDebug mode")
            print("\t-h\tHelp")
            sys.exit(0)

        texte_a_corriger = sys.argv[len(sys.argv)-1]
        texte_corrige_01 = corriger_orthographe_01(texte_a_corriger)
        console.print(highlight_differences("spellchecker :\t", texte_a_corriger, texte_corrige_01))
        console.print(get_highlighted_differences_counter("spellchecker :\t", texte_a_corriger, texte_corrige_01))

        texte_corrige_02 = corriger_orthographe_02(texte_a_corriger)
        console.print(highlight_differences(" hunspell    :\t", texte_a_corriger, texte_corrige_02))
        console.print(get_highlighted_differences_counter(" hunspell    :\t", texte_a_corriger, texte_corrige_02))

        texte_corrige_03 = corriger_orthographe_03(texte_a_corriger)
        console.print(highlight_differences("LanguageTool :\t", texte_a_corriger, texte_corrige_03))
        console.print(get_highlighted_differences_counter("LanguageTool :\t", texte_a_corriger, texte_corrige_03))

    else:

        # Exemple d'utilisation
        texte_faux =    "Voici un exenple de texte, de l'auteur François Martin, avic moins de 24 fotes d'ortographe."
        texte_correct = "Voici un exemple de texte, de l'auteur François Martin, avec moins de 24 fautes d'orthographe."
        console.print(highlight_differences("Texte ok   :\t",texte_correct, texte_correct, style_ok="bold white"))
        console.print(get_highlighted_differences_counter("Texte ok   :\t", texte_correct, texte_correct, style_ok="bold white"))

        console.print(highlight_differences("Texte faux :\t",texte_correct, texte_faux , style_ok="white"))
        console.print(get_highlighted_differences_counter("Texte faux :\t", texte_correct, texte_faux, style_ok="white"))

        texte_corrige_01 = corriger_orthographe_01(texte_faux)
        console.print(highlight_differences("spellchecker :\t", texte_correct,texte_corrige_01))
        console.print(get_highlighted_differences_counter("spellchecker :\t", texte_correct, texte_corrige_01))

        if GoDEBUG:
            different_words = compare_phrases(texte_corrige_01, texte_correct)
            for diff in different_words:
              print(f"Opération : {diff['operation']}")
              print(f"Texte incorrect : {diff['original_text']}")
              print(f"Texte correct : {diff['modified_text']}")
              print(diff)

        texte_corrige_02 = corriger_orthographe_02(texte_faux)
        console.print(highlight_differences(" hunspell    :\t", texte_correct, texte_corrige_02))
        console.print(get_highlighted_differences_counter(" hunspell    :\t", texte_correct, texte_corrige_02))

        texte_corrige_03 = corriger_orthographe_03(texte_faux)
        console.print(highlight_differences("LanguageTool :\t", texte_correct, texte_corrige_03, ))
        console.print(get_highlighted_differences_counter("LanguageTool :\t", texte_correct, texte_corrige_03))
