# CSS Specificity

1. inline
2. id
3. class
4. type

## <span style="color:red;">Hello</span> will be <span style="color:red;">red</span> not <span style="color:blue;">blue</span> ID is more specific.

```
<div id="foo">
    hello!
</div>
--------------------------------------------------------------------------------
div {
    color: blue;
}
#foo {
    color: red;
}
```

## Order also doesn't matter. <span style="color:red;">Hello</span> will be <span style="color:red;">red</span> not <span style="color:blue;">blue</span> ID is more specific.

```
<div id="foo">
    hello!
</div>
--------------------------------------------------------------------------------
#foo {
    color: red;
}
div {
    color: blue;
}
```

# Selectors
`a,b` - Multiple element selector  
`a b` - Descendant Selector  
`a > b` - Child Selector  
`a + b` - Adjecent Sibling Selector  
`[a=b]` - Atribute Selector  
`a:b` - Pseudoclass Selector  
`a::b` - Pseudoelement Selector  