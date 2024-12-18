import re
from spellchecker import SpellChecker
import hunspell
import language_tool_python
from difflib import SequenceMatcher


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
    return ' '.join(mots_corriges)


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


# Exemple d'utilisation
texte_faux = "Voici un exenple de texte, de l'auteur François Martin avic moins de 2004 fotes d'ortographe."
print(f"Texte faux   :\t {texte_faux}")
texte_corrige_01 = corriger_orthographe_01(texte_faux)
print(f"spellchecker :\t {texte_corrige_01}")

differences = compare_phrases(texte_faux, texte_corrige_01)
for diff in differences:
  print(f"Opération : {diff['operation']}")
  print(f"Texte incorrect : {diff['false_text']}")
  print(f"Texte correct : {diff['correct_text']}")
  print(diff)

texte_corrige_02 = corriger_orthographe_02(texte_faux)
print(f" hunspell    :\t {texte_corrige_02}")
texte_corrige_03 = corriger_orthographe_03(texte_faux)
print(f"LanguageTool :\t {texte_corrige_03}")
