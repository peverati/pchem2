-- pdf-fixes.lua (runs after Quarto's own filters, see _quarto.yml)
-- 1. PDF: equation references as "Eq. (5.7)" instead of "Eq. 5.7", matching the
--    equation numbers, which are printed in parentheses. (On the website, Quarto
--    writes the references after the filters run, so quarto.css adds the parentheses.)
-- 2. All formats: drop the line break at the end of each answer choice of the study
--    questions (the two trailing spaces); in the PDF it added an empty line after each choice.

function RawInline(el)
  if el.format == "latex" then
    local t = el.text:gsub("^\\ref{(eq%-[^}]+)}$", "(\\ref{%1})")
    if t ~= el.text then el.text = t; return el end
  end
end

function OrderedList(el)
  for _, item in ipairs(el.content) do
    local last = item[#item]
    if last and (last.t == "Plain" or last.t == "Para") then
      local inl = last.content
      while #inl > 0 and (inl[#inl].t == "LineBreak" or inl[#inl].t == "Space" or inl[#inl].t == "SoftBreak") do
        inl:remove(#inl)
      end
    end
  end
  return el
end
