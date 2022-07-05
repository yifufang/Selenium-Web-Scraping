from selenium.webdriver.remote.webelement import WebElement

class element_has_css_value(object):
    def __init__(self, locator, css_property, css_value):
        self.locator = locator
        self.css_property = css_property
        self.css_value = css_value

    def matchPropertyAndValue(self, css_property, css_value):
        return css_property == self.css_property and css_value  == self.css_value

    def extractPropertyAndValue(self, cssStatement):
        keyValue = cssStatement.split(':')
        if len(keyValue) == 2:
            key = keyValue[0].strip()
            value = keyValue[1].strip()
            return (key, value)
        return (None, None)

    def findProperty(self, entries):
        foundProperty = False
        for entry in entries:
            (css_property, css_value) = self.extractPropertyAndValue(entry)
            if css_value is None:
                continue
            foundProperty = self.matchPropertyAndValue(css_property, css_value)
            if foundProperty:
                break
        return foundProperty

    def __call__(self, driver):
        element = driver.find_element(*self.locator)
        styles = element.get_attribute("style")
        entries = styles.split(';')
        foundProperty = self.findProperty(entries)

        if foundProperty:
            return element
        else:
            return False