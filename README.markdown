HTMLOutliner
============

I'm busy producing HTML mockups/templates at the moment, and finding that it's
a real pain in the ass to have meaningful discussions about a page's structure
when it's full of dummy text.  The "content" simply overwhelms the markup, and
moreover makes it simply impossible to print (if Norm's taught me anything, he
certainly beat it into my head that a printed copy is essential for review).

HTMLOutliner is a toy Python project, really just a slight tweaking of work
that BeautifulSoup is already doing brilliantly.  It pretty-prints an HTML
document after removing all the text nodes that would otherwise distract from
the pure flow of the markup.  Attributes may, or may not, be displayed,
depending on your needs.

In short, it turns:

    <div class="module">
        <div class="hd">
            <h3>This is a module title</h3>
            <ul>
                <li>I like lists!</li>
                <li>Totally!</li>
            </ul>
        </div>
        <div class="bd">
            <p>This is a paragraph of text!</p>
            <p>Look at how much text it contains!</p>
        </div>
    </div>

into:

    <div class="module">
        <div class="hd">
            <h3></h3>
            <ul>
                <li></li>
                <li></li>
            </ul>
        </div>
        <div class="bd">
            <p></p>
            <p></p>
        </div>
    </div>

Enjoy.

TODO
----

*   Determine some way to reasonably label sections of the document.  Comment
    blocks seem like a reasonable way to make this happen.

*   Look for ways to bind placeholder text to an element.  It would be nice if
    I could end up with something like `<h1>Page Title</h1>` at the end of the
    day.  That dovetails with the labeling TODO nicely.
