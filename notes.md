So unpacking the pdfs into pages is going to be a bit of a tricky thing.

So a few documents have an extension in the mods file that looks like so

<extension>
<docClass>FR</docClass>
<accessId>FR-1992-01-02</accessId>
<volume>57</volume>
<issue>1</issue>
<isDigitizedFR>true</isDigitizedFR>
<printPageRange first="1" last="172" offset="8"/>
</extension>

Notice the offset is useful for getting around the front matter where regulations don't live.

This seems to cover quite a range of data

<extension>
<docClass>FR</docClass>
<accessId>FR-1938-04-15</accessId>
<volume>3</volume>
<issue>74</issue>
<isDigitizedFR>true</isDigitizedFR>
<printPageRange first="891" last="897" offset="0"/>
</extension>

Note that this document is from 1938

On the other hand

file:///Users/blibgober/Github/fr_by_page/mods_files/FR-2000-01-18.mods.xml

This is a problem, it doesn't have the extension above. What it has instead is a part like so

<part type="Contents">
<extent unit="pages">
<start>I</start>
<end>VII</end>
</extent>
</part>

that you can use to figure out the offset. Maybe this is fine.

But this is wierd

https://www.govinfo.gov/metadata/pkg/FR-1980-07-28/mods.xml

Goes right in the middle of the 1980 and 1992 document and does not have an offset. It does have a printPageRange and appears to start right away, no front matter. So maybe this is ok

So I think the first thing to do is to figure out how complete the print page range is, and if it is missing why it is missing.

Ok the analysis concluded

Contiguous date ranges:
1936-03-14 00:00:00 to 1994-04-25 00:00:00 - with printPageRange
1994-04-25 00:00:00 to 1994-04-25 00:00:00 - without printPageRange
1994-04-26 00:00:00 to 1994-10-31 00:00:00 - with printPageRange
1994-11-01 00:00:00 to 1994-11-01 00:00:00 - without printPageRange
1994-11-02 00:00:00 to 1994-11-14 00:00:00 - with printPageRange
1994-11-14 00:00:00 to 1994-11-14 00:00:00 - without printPageRange
1994-11-15 00:00:00 to 1994-12-30 00:00:00 - with printPageRange
1995-01-03 00:00:00 to NaT - without printPageRange
Contiguous date ranges saved to contiguous_date_ranges.csv

So basically we can hot fix 3 PDF for the weird ones in the 1994 period that did not
have the page range thing.

