# -*- coding: utf-8 -*-

# PyQt library
from aqt.qt import *
import aqt.qt as QtGui
from PyQt4 import QtCore
from PyQt4 import QtWebKit
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QApplication, QCursor
from addon import collection
from libdict import macmillan
import re
import datetime
from addon.collection import get_plugin


class StyleSheet(object):
    """Needed for html elements embedded into labels."""
    related_link_key = "font-weight: bold; color: rgb(10, 50, 10);"
    related_link_part_of_speech = "font-weight: normal; color: grey;"
    custom_example_default_text = "QLineEdit {color: gray; font-style: italic}"
    custom_example_user_text = "QLineEdit {color: black; font-style: normal}"
    user_example_style = "text-decoration: none; color: rgb(0, 133, 31);"


def tostr(a):
    if a is None:
        return ""
    else:
        return a


class SelectDeckComboBox(QComboBox):
    def __init__(self):
        super(SelectDeckComboBox, self).__init__()
        self.addItems(get_plugin().get_deck_names())
        self.setCurrentIndex(0)

    def showPopup(self):
        # update the list...
        self.clear()
        self.addItems(get_plugin().get_deck_names())
        super(SelectDeckComboBox, self).showPopup()


class DictWindow(QWidget):
    def init_begin(self):
        def conf_btn(btn):
            btn.setMaximumWidth(60)
            btn.setStyleSheet("font-weight: bold; font-family: monospace")
        self.search_input = QLineEdit("")
        self.search_button = QPushButton("SEARCH")
        self.prev_button = QPushButton("<-")
        self.next_button = QPushButton("->")
        self.prev_button.setEnabled(False)
        self.next_button.setEnabled(False)
        self.prev_button.setMaximumWidth(66)
        self.next_button.setMaximumWidth(66)
        self.wordlist_button = QPushButton("WORDLIST")
        conf_btn(self.prev_button)
        conf_btn(self.next_button)
        self.select_deck_label = QLabel("DECK: ")
        self.select_deck_combobox = SelectDeckComboBox()

    def init_end(self):
        self.head_hbox = QHBoxLayout()
        self.head_hbox.addWidget(self.prev_button)
        self.head_hbox.addWidget(self.next_button)
        self.head_hbox.addWidget(self.search_input)
        self.head_hbox.addWidget(self.search_button)
        self.head_hbox.addWidget(self.wordlist_button)
        self.head_hbox.addWidget(self.select_deck_label)
        self.head_hbox.addWidget(self.select_deck_combobox)

        self.main_vbox = QVBoxLayout()
        self.main_vbox.addLayout(self.head_hbox)
        self.main_vbox.addWidget(self.current_view)
        self.setLayout(self.main_vbox)
        self.resize(800,600)
        self.setWindowTitle('Macmillan Dictionary')

    def closeEvent(self, event):
        event.ignore()
        self.hide()
    
    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            # Selecting the search input field
            self.search_input.setFocus()
            self.search_input.setText("")


class ScrollWidget(QWidget):
    pass


class LinkLabel(QLabel):
    clicked = pyqtSignal()
    def __init__(self, *args, **kwargs):
        super(LinkLabel, self).__init__(*args, **kwargs)
        self.setCursor(Qt.PointingHandCursor)

    def mouseReleaseEvent(self, e):
        self.clicked.emit()


class DictEntryView(QWidget):
    def init_begin(self):
        self.left_scroll = QScrollArea()
        self.right_scroll = QScrollArea()
        self.left_widget = ScrollWidget()
        self.right_widget = ScrollWidget()
        self.left_vbox = QVBoxLayout()
        self.right_vbox = QVBoxLayout()
        self.main_hbox = QHBoxLayout()

    def add_sense_widget(self, w):
        self.left_vbox.addWidget(w)

    def add_link(self, link, callback):
        title = tostr(link.key)
        href = link.url
        label_content = "<span style='"+StyleSheet.related_link_key+"'>" + tostr(link.key) + "</span> "
        label_content += "<span style='"+StyleSheet.related_link_part_of_speech+"'>"
        label_content += tostr(link.part_of_speech)
        # label_content += " " + tostr(link.url)
        label_content += "</span>"
        btn = LinkLabel(label_content)
        btn.clicked.connect(callback)
        btn.show()
        btn.setWordWrap(True)
        def make_line():
            fr = QFrame()
            #fr.setStyleSheet("background-color: white;");
            fr.setFrameShape(QFrame.HLine)
            fr.setFrameShadow(QFrame.Sunken)
            fr.setLineWidth(2)
            #fr.setMidLineWidth(1)
            return fr
        self.right_vbox.addWidget(btn)
        self.right_vbox.addWidget(make_line())

    def init_end(self):
        self.left_scroll.setWidgetResizable(True)
        self.right_scroll.setWidgetResizable(True)
        self.left_widget.setLayout(self.left_vbox)
        self.right_widget.setLayout(self.right_vbox)
        self.left_widget.show()
        self.right_widget.show()
        self.left_scroll.setWidget(self.left_widget)
        self.right_scroll.setWidget(self.right_widget)
        self.right_scroll.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.right_scroll.setMaximumWidth(get_plugin().config.related_defs_panel_width)
        self.main_hbox.addWidget(self.left_scroll)
        self.main_hbox.addWidget(self.right_scroll)
        self.setLayout(self.main_hbox)


class ExampleAddButton(QPushButton):
    def __init__(self):
        super(ExampleAddButton, self).__init__("+")


class ExampleWidget(QWidget):
    def __init__(self, example, callback, user_defined=False):
        super(ExampleWidget, self).__init__()
        key = example.format_original_key_html()
        ex = example.content
        if not user_defined:
            label_content = '<span style="'+get_plugin().config.example_style+'"><i>'
        else:
            label_content = '<span style="'+StyleSheet.user_example_style+'"><i>'
        if key:
            label_content += "</i><b> "+key+" </b><i>"
        label_content += ex
        label_content += "</i></span>"
        self.label = QLabel(label_content)
        self.label.setWordWrap(True)
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)

        self.button = ExampleAddButton()
        self.button.clicked.connect(callback)
        self.button.clicked.connect(lambda: self.button.setEnabled(False))

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.button)
        layout.addWidget(self.label)
        self.setLayout(layout)


class UserExampleLineEdit(QLineEdit):
    DEFAULT_TEXT = "Type your example usage of this word here..."
    def focusInEvent(self, e):
        super(UserExampleLineEdit, self).focusInEvent(e)
        if self.text() == self.DEFAULT_TEXT:
            self.setText("")
            self.setStyleSheet(StyleSheet.custom_example_user_text)

    def focusOutEvent(self, e):
        if e is not None:
            super(UserExampleLineEdit, self).focusOutEvent(e)
        if self.text() == "":
            self.setText(self.DEFAULT_TEXT)
            self.setStyleSheet(StyleSheet.custom_example_default_text)

    def __init__(self):
        super(UserExampleLineEdit, self).__init__("")
        self.focusOutEvent(None)


class UserExampleWidget(QWidget):
    def __init__(self, callback):
        super(UserExampleWidget, self).__init__()
        self.lineedit = UserExampleLineEdit()
        self.button = ExampleAddButton()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.button)
        layout.addWidget(self.lineedit)
        self.setLayout(layout)
        self.callback = callback
        self.button.clicked.connect(self.return_pressed)
        self.lineedit.returnPressed.connect(self.return_pressed)
        self.lineedit.textChanged.connect(self.text_changed)
        self.button.setEnabled(False)

    def text_changed(self, txt):
        if txt == '' or txt == self.lineedit.DEFAULT_TEXT:
            self.button.setEnabled(False)
        else:
            self.button.setEnabled(True)

    def return_pressed(self):
        self.callback(self.lineedit.text())
        self.lineedit.clear()
        self.lineedit.clearFocus()
        self.lineedit.focusOutEvent(None)


class HiddenExamplesWidget(QWidget):
    def __init__(self, examples_list):
        super(HiddenExamplesWidget, self).__init__()
        self.setMouseTracking(True)
        self.update(examples_list)

    def update(self, example_widgets):
        self.main_layout = QVBoxLayout()
        for i in example_widgets:
            self.main_layout.addWidget(i)
        self.ellipsis = QLabel('<a href="example" style="'+
            get_plugin().config.example_style+'"><b> ... ... ... </b></a>')
        self.main_layout.addWidget(self.ellipsis)
        self.setLayout(self.main_layout)
        self.main_layout.setMargin(2)
        self.example_widgets = example_widgets
        self.hidden_example_widgets = example_widgets[
            (get_plugin().config.max_examples_per_sense):]
        self.show()
        self.ellipsis.hide()
        self.collapse()

    def insert_example_one_before_end(self, ex_widget):
        self.main_layout.insertWidget(self.main_layout.count()-2, ex_widget)
        self.example_widgets.insert(len(self.example_widgets)-1, ex_widget)
        self.hidden_example_widgets = self.example_widgets[
            (get_plugin().config.max_examples_per_sense):]
        self.show()
        self.ellipsis.hide()
        self.collapse()

    def expand(self):
        # here showing examples
        for i in self.hidden_example_widgets:
            i.show()
        self.ellipsis.hide()

    def collapse(self):
        # here hiding examples
        for i in self.hidden_example_widgets:
            i.hide()
        if self.hidden_example_widgets != []:
            self.ellipsis.show()

    def mouseMoveEvent(self, event):
        super(HiddenExamplesWidget, self).mouseMoveEvent(event)
        if event.x() < get_plugin().config.examples_hover_area_width:
            self.expand()
        else:
            self.collapse()


class SenseWidget(QFrame):
    def format_definition_html(self):
        wyn = ""
        if self.sense.style_level != "" and self.sense.style_level != None:
            wyn += "<i>"+self.sense.style_level+"</i>"
        return wyn + " " + self.sense.definition

    def format_erased_definition_html(self):
        wyn = ""
        if self.sense.style_level != "" and self.sense.style_level != None:
            wyn += "<i>"+self.sense.style_level+"</i>"
        tmp_def = self.sense.definition
        keys = self.extract_keys()
        for i in keys:
            tmp_def = " ____ ".join(tmp_def.split(i))
        return wyn + tmp_def

    def init_begin(self):
        self.main_layout = QVBoxLayout()
        
        self.main_layout.setMargin(0)
        self.main_layout.setSpacing(0)
        
        self.label = QLabel(self.sense.format_key_html() + "  ---  " + self.format_definition_html())
        self.label.setWordWrap(True)
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        self.label.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        self.main_layout.addWidget(self.label)

        self.example_widgets = []

    def add_example(self, example):
        # tej lambdy NIE można uprościć, bo inaczej się zbuguje:
        self.example_widgets.append(ExampleWidget(example, (
            lambda t: lambda: get_plugin().add_note_example(t))(example)))

    def make_user_example_widget(self, example):
        return ExampleWidget(
            example,
            (lambda t: lambda: get_plugin().add_note_example(t))(example),
            user_defined=True,
        )

    def add_textfield_for_custom_examples(self):
        self.example_widgets.append(UserExampleWidget(self.user_example_supplied))

    def user_example_supplied(self, text):
        ex = get_plugin().create_user_example(self.sense, text)
        ex_w = self.make_user_example_widget(ex)

        self.examples_widget.insert_example_one_before_end(ex_w)

        ex_w.button.clicked.emit(True)

    def init_end(self):
        self.examples_widget = HiddenExamplesWidget(self.example_widgets)
        self.main_layout.addWidget(self.examples_widget)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        self.setLayout(self.main_layout)
        self.show()

    def leaveEvent(self, event):
        super(SenseWidget, self).leaveEvent(event)
        self.examples_widget.collapse()


class WordListView(QWidget):
    def init_begin(self):
        self.main_hbox = QHBoxLayout()
        self.text_edit = QTextEdit()
        self.text_edit.setHtml('<table border="2" style="border-color: black; border-width: 2; border-style: solid;"> </table>')
        self.main_hbox.addWidget(self.text_edit)
        self.setLayout(self.main_hbox)
        def func_constr(f):
            def wyn(e):
                f(e)
                if e.key() == QtCore.Qt.Key_Backspace:
                    self.reload_table()
            return wyn
        self.text_edit.keyPressEvent = func_constr(self.text_edit.keyPressEvent)
        if get_plugin().config.log_wordlist:
            today = datetime.date.today()
            filename = "millandict_wordlist_log_"+str(today.month) + "_" +str(today.year) + ".html"
            self.logfile = filename

    def init_end(self):
        pass

    def add_table_row(self, a, b):
        tr = "<tr><td>" + a + "</td><td>" + b + "</td></tr>"
        text = self.text_edit.toHtml()[:-(len("</table></body></html>"))] + tr + "</table></body></html>"
        text = 'border="2"'.join(text.split('border="0"'))
        self.text_edit.setHtml(text)
        if get_plugin().config.log_wordlist:
            with open(self.logfile, "a+") as f:
                f.write(tr.encode("ascii","ignore") + "\n")
        #print self.text_edit.toHtml()

    def reload_table(self):
        text = self.text_edit.toHtml()
        text = 'border="2"'.join(text.split('border="0"'))
        #text = ''.join(text.split('<td></td>'))
        text = ''.join(re.split(r'<tr>\s*<td>\s*</td>\s*<td>\s*</td>\s*</tr>',text))
        #print text
        cursor = self.text_edit.textCursor()
        c_pos = self.text_edit.cursorRect().center()
        self.text_edit.setHtml(text)
        self.text_edit.setTextCursor(self.text_edit.cursorForPosition(c_pos))
