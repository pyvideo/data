 # Schema for Video Record.

[PyVideo.org](https://pyvideo.org) runs on github and every video is described by some json code based on the [official schema](https://github.com/pyvideo/data/blob/master/.schemas/video.json).

The following are some samples of how this file should look like.

```json
{
  "copyright_text": null,
  "description": "",
  "duration": 1667,
  "language": "eng",
  "recorded": "2019-05-10",
  "related_urls": [
    {
      "label": "Conference schedule",
      "url": "https://pydata.org/amsterdam2019/schedule/"
    }
  ],
  "speakers": [
    "Ritchie Vink"
  ],
  "tags": [
    "pydata"
  ],
  "thumbnail_url": "https://i.ytimg.com/vi/mIAeSDcM1zg/maxresdefault.jpg",
  "title": "Build Facebook's Prophet in PyMC3",
  "videos": [
    {
      "type": "youtube",
      "url": "https://www.youtube.com/watch?v=mIAeSDcM1zg"
    }
  ]
}

{
  "description": "Day 3, R2 11:30\u201312:00\n\nToday, there are many tasks to repeat in the company/community.\r\nIn addition, we often use chat such as Slack for daily communication.\r\nSo, I created a chatbot([PyCon JP Bot](https://github.com/pyconjp/pyconjpbot)) to automate various boring tasks related to holding PyCon JP.\r\n\r\nIn this talk, I will first explain how to create a chatbot using [slackbot](https://github.com/lins05/slackbot).\r\nI will tell you how to registers bot's integration on Slack and how to create a simple bot in Python that responds to specific keywords.\r\n\r\nAnd as a specific case, I will explain how to make a bot command to perform the following operations and technical problems.\r\n\r\n- Emoji reaction\r\n- Calculator: SymPy\r\n- Karma(plusplus): Peewee\r\n- Search issues, display issue details: JIRA API\r\n- Create multiple issues from a template: JIRA API, Sheets Spreadsheet API\r\n- Search files from Google Drive: Google Drive API\r\n- Account management of G Suite(user, alias, group and member): G Suite API\r\n- etc.\n\nSlides: https://gitpitch.com/takanory/slides?p=20190922pycontw#/\n\nSpeaker: Takanori Suzuki\n\nTakanori is a Vice Chairperson of PyCon JP Committee(www.pycon.jp).\r\nHe is also a director of BeProud Inc.(www.beproud.jp), and his title is \"Python Climber\".\r\nTakanori held PyCon JP 2014 to 2016 as the chairperson.\r\nCurrently he teaches Python to beginners as a lecturer at Python Boot Camp(pycamp.pycon.jp) all over Japan.\r\nIn addition, he published several Python books.\r\nTananori plays trumpet, climbs boulder, loves Lego, ferrets and beer.",
  "recorded": "2019-09-22",
  "speakers": [
    "Takanori Suzuki"
  ],
  "thumbnail_url": "https://i.ytimg.com/vi/XGHR4D8_fjQ/hqdefault.jpg",
  "title": "Automate the Boring Stuff with Slackbot",
  "videos": [
    {
      "type": "youtube",
      "url": "https://www.youtube.com/watch?v=XGHR4D8_fjQ"
    }
  ]
}
```

## copyright_text
This parameter is optional. It should have the text of the license under which the media is being shared or a link to a license if it exists. The copyright_text may also be "null"
#### examples
```json
{
    "copyright_text" : null
}
{
    "copyright_text" : "THIS VIDEO AND THE SOFTWARE IT DESCRIBES IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE."
}
{
    "copyright_text" : "https://opensource.org/licenses/AGPL-3.0"
}
```
## description
This is an optional field that is used to provide information about the video being shared. It can be `null`, `plain text` or `reStructuredText`. If you are interested in knowing how `reStructuredText` works here is the [documentation](http://docutils.sourceforge.net/rst.html).
### examples
```json
{
    "description" : null
}
{
    "description" : "DjangoCon 2019 - Just Add Await: Retrofitting Async Into Django by Andrew Godwin\n\nWriting async code from scratch is hard; trying to add it into a large, existing framework is harder. Learn about the problems we face trying to make Django async while maintaining backwards compatibility, as well as the problems maintaining hybrid sync-and-async Python codebases in general.\n\nThis talk was presented at: https://2019.djangocon.us/talks/just-add-await-retrofitting-async-into/\n\nLINKS:\nFollow Andrew Godwin \ud83d\udc47\nOn Twitter: https://twitter.com/andrewgodwin\nOfficial homepage: http://www.aeracode.org\n\nFollow DjangCon US \ud83d\udc47\nhttps://twitter.com/djangocon\n\nFollow DEFNA \ud83d\udc47\nhttps://twitter.com/defnado\nhttps://www.defna.org/\n\nIntro music: \"This Is How We Quirk It\" by Avocado Junkie.\nVideo production by Confreaks TV.\nCaptions by White Coat Captioning."
}
{
    "description" : "Day 3, R2 10:50\u201311:20\n\nThe SQL client is *ubiquitous* and **impossible** for developers not to have one in their toolbag. However potentially there is a unforeseen situation that the developers are forbid to use SQL client to access the cloud/on-premise SQL DB. This proposal primarily addresses the issue of such scenario and provides a solution based on the hacker's mindset. In this proposal, the author will show how he tackles this pain point in his workplace, by creating a universal SQL client CLI that allows him to connect to the SQL DB in his DB cluster, hence extends this project to other SQL DB using the API standardization in PEP 249. Apart from integrating all the SQL connectors, the author also implemented standardize hotkey for all the SQL DB, by studying the internal core of the SQL standards, and retrieving SQL metadata using pure SQL queries through the hotkeys.\n\nSlides not uploaded by the speaker.\n\nSpeaker: Ing Wei Tang\n\nIng Wei is the chair for PyCon MY 2019, the co-chair of PyCon MY 2018, and vice president of MyPOP. He has spoken in various PyCons, particularly in PyCon APAC 2018, as well as involving in PyCon communities actively in Malaysia.\r\n\r\nHe uses python a lot in his daily work, especially coding the automation process and flow. During his past time, he likes to experience and perform hacking different things on operating system level.\r\n\r\nApart from programming language, he can also speak 5 different types of languages concurrently in one sentence. Please ask for demo if time permits."
}
```
## duration
This is an optional parameter. This is the duration of the video in seconds.
### examples
```json
{
    "duration" : null
}
{
    "duration" : 2368
}
```
## language
This is an optional parameter. This is the language of the video represented using the [ISO 639-3](https://iso639-3.sil.org/) code. If you are looking for a more accessible list try [this](https://en.wikipedia.org/wiki/Wikipedia:WikiProject_Languages/List_of_ISO_639-3_language_codes_(2019)) one
### examples
```json
{
    "language" : "eng"
}
{
    "language" : "fra"
}
{
    "language" : "deu"
}
```
## quality_notes
This is an optional parameter. You can use this section to provide some notes on the quality of the video.
### examples
```json
{
    "quality_notes" : null
}
{
    "quality_notes" : "Great audio and sound"
}
{
    "quality_notes" : "Sound is poor for the first 13 minutes but is better after that"
}
```
## recorded
This is a required parameter. Provide the date the video was recorded in ISO-8601 format i.e. `(YYYY-MM-DD[Thh:mm:ss[+hh:mm]])`
### examples
```json
{
    "recorded" : null
}
{
    "recorded" : "2008-09-06"
}
    "recorded" : "2019-08-10T13:33:30+05:30"
}
```
## related_urls
This is an optional parameter. This is a list of URLs to resources that are related to the video.
### examples
```json
{
    "related_urls": [
                      "https://www.tensorflow.org/tutorials",
                      "https://bit.ly/tf-ws1",
                      "https://bit.ly/tf-ws3",
                      "https://bit.ly/tf-ws4",
                      "https://bit.ly/tf-ws4a"
                      ]
}                     
{
      "related_urls": [
    {
      "label": "Conference schedule",
      "url": "https://us.pycon.org/2018/schedule/talks/"
    },
    {
      "label": "Conference slides (Github)",
      "url": "https://github.com/PyCon/2018-slides"
    },
    {
      "label": "Conference slides (SpeakerDeck)",
      "url": "https://speakerdeck.com/pycon2018"
    }
  ],
}
```
## slug
This is an optional parameter. Provide a web safe [slug](https://en.wikipedia.org/wiki/Clean_URL#Slug) of the video.
### example
```json
{
    "slug" : "what-happened-at-aaronswhack"
}
```
## speakers
This is a required parameter. This is an array of the speakers in the video arranged in alphabetical order based on the last name of the speakers.
### examples
```json
{
    "speakers": ["Eugenio Llanos"]
}
{
    "speakers": [ "James Bednar", 
                  "Philipp Rudiger", 
                  "Julia Signell",
                  "Jean-Luc Stevens"
                ],
}
```
## summary
This is an optional parameter. A short description of the video. It may be in plain text or reStructuredText.
### example
```json
{
    "summary" : null
}
{
    "summary" : "I came to coding by a circuitous route that started with studying logic within philosophy. Along the way, I've tackled a number of subjects related to learning and skill development - from a philosophical, practical, sociological and educational standpoint - and I thought, what better way to test the things I've come away with in action than to put them to work for me as I start to learn how to code.\n\nI\u2019ll be providing a brief summary of the what and why of things that worked and things that didn't work to help me learn and become a better coder as I started teaching myself, and continue leaning, Python. Rather than focusing on issues that are aimed at beginners, I want to zero in on a few points that I want to take into my late coding career and so will be helpful to a broader audience as they are picking up newer technologies. I'll quickly move through things like mapping out code before writing it, being efficient and descriptive, how to deal with failure when it inevitably happens, contrarianism in the coding community, how to \"\"stick to it\"\", Googling, dealing with the peaks and valleys of daily coding, ego and code, pacing yourself, taking 'productive' breaks, and how to gauge improvement."
}
```
## thumbnail_url
This is an optional parameter. It is the url to the initial thumbnail of the video.
### examples
```json
{
    "thumbnail_url" : null
}
{
    "thumbnail_url" : "https://i.ytimg.com/vi/borv_KMI9Ac/hqdefault.jpg"
}
```
## title
This is a required parameter. It is the title that will be used for the video.
### examples
```json
{
    "title" :  "Sparkling Pandas- Letting Pandas Roam on Spark DataFrames"
}
{
    "title" : "Visualize any Data Easily, from Notebooks to Dashboards"
}
```
## videos
This is a required parameter. It is an array showing the video locations and types.
### examples
```json
{
    "videos" : [
    {
      "type": "youtube",
      "url": "https://www.youtube.com/watch?v=7deGS4IPAQ0"
    }
  ]
}
{
    "videos" :  [
    {
      "type": "vimeo",
      "url": "https://vimeo.com/271025957"
    }
  ]
}
{
    "videos" :  [
    {
      "type": "ogv",
      "url": "http://video-pyconfr2015.paulla.asso.fr/009%20-%20Charlie%20Clark%20-%20The%20Art%20of%20Doing%20Nothing%20-%20Using%20profiling%20to%20speed%20up%20your%20code.ogv"
    },
    {
      "type": "mp4",
      "url": "http://video-pyconfr2015.paulla.asso.fr/009%20-%20Charlie%20Clark%20-%20The%20Art%20of%20Doing%20Nothing%20-%20Using%20profiling%20to%20speed%20up%20your%20code.mp4"
    },
    {
      "type": "webm",
      "url": "http://video-pyconfr2015.paulla.asso.fr/009%20-%20Charlie%20Clark%20-%20The%20Art%20of%20Doing%20Nothing%20-%20Using%20profiling%20to%20speed%20up%20your%20code.webm"
    }
  ]
}
```
