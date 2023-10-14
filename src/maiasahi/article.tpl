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

{% raw %}
{{< sortabletable >}}
{% endraw %}
{{ vocabulary }}
{% raw %}
{{< /sortabletable >}}
{% endraw %}

## Grammar and Sentence Structure

{{ grammar }}