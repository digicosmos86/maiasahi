---
title: {{ title }}
date: {{ date }}
slug: {{ slug }}
---

![{{ caption }}]({{ figure }} "{{ caption }}")

[Link to the original article]({{ link }})

{% raw %}
{{< rawhtml >}}
<div>
{% endraw %}
{{ article }}
{% raw %}
</div>
{{< /rawhtml >}}
{% endraw %}

## Vocabulary

{{ vocabulary }}

## Grammar and Sentence Structure

{{ grammar }}