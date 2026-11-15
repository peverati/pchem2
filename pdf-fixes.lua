-- pdf-fixes.lua (runs after Quarto's own filters, see _quarto.yml)
-- 1. PDF: equation references as "Eq. (5.7)" instead of "Eq. 5.7", matching the
--    equation numbers, which are printed in parentheses. (On the website, Quarto
--    writes the references after the filters run, so quarto.css adds the parentheses.)
-- 2. All formats: drop the line break at the end of each answer choice of the study
--    questions (the two trailing spaces); in the PDF it added an empty line after each choice.
-- 3. Study questions: hanging indent for questions that wrap (see below).

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

-- 3. Study questions ("**1. Question text?**"): hanging indent, so that a question that
--    wraps to a second line is aligned with the text after its number, not with the number.
--    PDF: the number in a fixed-width box, then the question indented; website: CSS class .question.
local QW = "1.7em"
function Para(el)
  local first = el.content[1]
  if not (first and first.t == "Strong") then return nil end
  local num = first.content[1]
  if not (num and num.t == "Str" and num.text:match("^%d+%.$")) then return nil end
  if FORMAT:match("latex") then
    local rest = {}
    for k = 2, #first.content do rest[#rest + 1] = first.content[k] end
    while #rest > 0 and (rest[1].t == "Space" or rest[1].t == "SoftBreak") do table.remove(rest, 1) end
    local inl = {pandoc.RawInline("latex",
      "\\par\\medskip\\noindent\\hangindent=" .. QW .. "\\hangafter=1\\makebox[" .. QW .. "][l]{\\textbf{" .. num.text .. "}}"),
      pandoc.Strong(rest)}
    for k = 2, #el.content do inl[#inl + 1] = el.content[k] end
    return pandoc.Para(inl)
  elseif FORMAT:match("html") then
    return pandoc.Div({el}, pandoc.Attr("", {"question"}))
  end
end
