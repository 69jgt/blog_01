from django import template
import readtime

register = template.Library()

# Readtime calculates the time some text takes the average human to read
def read(html):
    return readtime.of_html(html)

register.filter('readtime',read)