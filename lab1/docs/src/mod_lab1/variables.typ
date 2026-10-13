#let discipline = "Моделирование"
#let teacher = "Тропченко А. А."

#let lab = (
  number: 1,
  name: [Обработка результатов измерений: статистический анализ числовой последовательности],
  variant: [205]
)

#let student = (
  name: "Карнажицкий Максим Романович",
  group: "P3311"
)

#let footerData = (
  city: "Санкт-Петербург",
)

#let code_block(
  code,
  background: rgb("#f0f0f0"),
  inset: 10pt,
  radius: 4pt,
  show-line-numbers: false
) = {
  block(
    fill: background,
    inset: inset,
    radius: radius,
    width: 100%,
    stroke: 0.5pt + rgb("#d0d0d0"),
    {
      set text(font: "Fira Code", size: 9pt)
      // Проверяем тип: если это уже raw content, используем как есть
      if type(code) == content {
        code
      } else {
        // Если это строка, оборачиваем в raw
        if show-line-numbers {
          raw(code, lang: "bash", block: true)
        } else {
          raw(code, lang: "bash")
        }
      }
    }
  )
}

