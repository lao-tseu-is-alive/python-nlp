import re
from spellchecker import SpellChecker
import hunspell


def corriger_orthographe_01(texte):
    """
  Corrige les fautes d'orthographe dans un texte en français avec spellchecker.

  Args:
    texte: Le texte à corriger.

  Returns:
    Le texte corrigé.
  """
    # Séparer les mots et la ponctuation
    mots = re.findall(r'\w+|[^\w\s]', texte, re.UNICODE)

    # Corriger chaque mot
    mots_corriges = []
    for mot in mots:
      # Vérifier si le mot est mal orthographié
      if mot not in spell01:
        # Obtenir la correction
        correction = spell01.correction(mot)
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
  mots = texte.split()
  mots_corriges = []
  for mot in mots:
    if not spell02.spell(mot):
      suggestions = spell02.suggest(mot)
      if suggestions:
        mots_corriges.append(suggestions[0])
      else:
        mots_corriges.append(mot)
    else:
      mots_corriges.append(mot)
  return ' '.join(mots_corriges)


# Initialiser le correcteur orthographique spellchecker
spell01 = SpellChecker(language='fr')

# Initialize the Hunspell spell checker for French
spell02 = hunspell.HunSpell('/usr/share/hunspell/fr.dic', '/usr/share/hunspell/fr.aff')


# Exemple d'utilisation
texte_faux = "Ceci est un exenple de texte avic moins de 2004 fotes d'ortographe."
print(f"Texte faux   :\t {texte_faux}")
texte_corrige_01 = corriger_orthographe_01(texte_faux)
print(f"spellchecker :\t {texte_corrige_01}")
texte_corrige_02 = corriger_orthographe_02(texte_faux)
print(f" hunspell    :\t {texte_corrige_02}")
