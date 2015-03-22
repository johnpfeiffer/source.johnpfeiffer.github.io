Title: Markdown syntax cheatsheet
Date: 2014-07-02 20:21
Tags: markdown, html

[TOC]

### Markdown Syntax

- html <em\> is markdown `*emphasis* or _italics_` = *emphasis* or _italics_ 
- html <strong\> is markdown `**strong* or __bold__` = **strong** or __bold__
- html strikethrough is not supported but can just be `<del>strikethrough</del>` = <del>strikethrough</del>
- html <blockquote\> is markdown `>`
> at the start of each line
- html unordered list `<ul>` = `- item` or alternatives: `+ item` , `* item`
- html <hr /\> is markdown `- - -` or alternatives: `* * *` , `***` , `*****`
- html <a href= for hyper links is:

> `<http://blog.john-pfeiffer.com>` converts into a link that is automatically turned clickable:

> `<a href="http://johnpfeiffer.bitbucket.org">http://johnpfeiffer.bitbucket.org</a>`

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

:::text or :::bash at the top of a code block will control the syntax highlighting, see <http://pygments.org/docs/lexers>
    
# H1
`# H1`

###### H6
`###### H6`


### Tables are (sometimes) not supported but...

#### Table with left justified (GitHub Flavored Markdown)

    :::text
    |in|out|other|
    |---|---|---|
    |yes|no|maybe|

- - -

|in|out|other|
|---|---|---|
|yes|no|maybe|
|`<em>`|`*emphasis*`|*emphasis*

- - -

#### Table with text center aligned

    :::text
    |short|long centered|
    |:-:|:-:|
    |y|n|

- - -

|short|long centered|
|:-:|:-:|
|y|n|

- - -

#### HTML Table

    :::html
    <table><th>header</th>
      <tr>
        <td>first column in row 1</td><td>2nd column</td>
      </tr>
    </table>

- - -
### more info
<http://daringfireball.net/projects/markdown/syntax>

