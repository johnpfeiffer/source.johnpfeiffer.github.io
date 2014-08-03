Title: Markdown syntax cheatsheet
Date: 2014-07-02 20:21

- html &lt;em&gt; is markdown `*emphasis* or _italics_` = *emphasis* or _italics_ 
- html &lt;strong&gt; is markdown `**strong* or __bold__` = **strong** or __bold__
- html strikethrough is not supported but can just be `<del>strikethrough</del>` = <del>strikethrough</del>
- html &lt;blockquote&gt; is markdown `>` at the start of each line
- unordered list `- item` or alternatives: `+ item` , `* item`
- html &lt;hr /&gt; is markdown `- - -` or alternatives: `* * *` , `***` , `*****`
- html &lt;a href= for hyper links is:
> &lt;http://example.com&gt; is a link that is automatically turned clickable:
> <http://johnpfeiffer.bitbucket.org>  becomes &lt;a href="http://johnpfeiffer.bitbucket.org"&gt;http://johnpfeiffer.bitbucket.org&lt;/a&gt;
> `[an example](http://example.com/ "ExampleTitle")` [an example](/about-john-pfeiffer "ExampleTitle") 
- both absolute and relative links are supported, as well as reference links that are defined elsewhere:
`This is [an example][someid]`
> `[someid]: http://example.com/  "Optional Title Here"`
- - - 

1. numbered list `1` at the beginning of each line
> -     any digit will do, the numbering is rendered in order
> -     ensure the numbered list is surrounded by empty lines


**Inline code** is markdown \`backtick around the text\` = `backtick around the text`

**A code block** is markdown `indent 4 spaces or 1 tab`
> -    a blank line in the code block still needs to be indented
> -    ensure the code block is surrounded by empty lines
    


# H1  `# H1`
###### H6  `###### H6`

[more info](http://daringfireball.net/projects/markdown/syntax)

