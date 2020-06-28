from collections import defaultdict
import functools
import random

from IPython.display import clear_output, display
from ipywidgets import (Button,
                        Dropdown,
                        FloatSlider,
                        HBox,
                        HTML,
                        IntSlider,
                        Output,
                        Textarea)


def annotate(examples,
             options=None,
             shuffle=False,
             include_skip=True,
             display_fn=display):
    """
    Build an interactive widget for annotating a list of input examples.

    Parameters
    ----------
    examples: list(any), list of items to annotate
    options: list(any) or tuple(start, end, [step]) or None
             if list: list of labels for binary classification task (Dropdown or Buttons)
             if tuple: range for regression task (IntSlider or FloatSlider)
             if None: arbitrary text input (TextArea)
    shuffle: bool, shuffle the examples before annotating
    include_skip: bool, include option to skip example while annotating
    display_fn: func, function for displaying an example to the user

    Returns
    -------
    annotations : list of tuples, list of annotated examples (example, label)
    """
    examples = list(examples)
    if shuffle:
        random.shuffle(examples)

    annotations = []
    current_index = -1

    def set_label_text():
        nonlocal count_label
        count_label.value = '{} examples annotated, {} examples left'.format(
            len(annotations), len(examples) - current_index
        )

    def show_next():
        nonlocal current_index
        current_index += 1
        set_label_text()
        if current_index >= len(examples):
            for btn in buttons:
                btn.disabled = True
            print('Annotation done.')
            return
        with out:
            clear_output(wait=True)
            display_fn(examples[current_index])

    def add_annotation(annotation):
        annotations.append((examples[current_index], annotation))
        show_next()

    def skip(btn):
        show_next()

    count_label = HTML()
    set_label_text()
    display(count_label)

    if type(options) == list:
        task_type = 'classification'
    elif type(options) == tuple and len(options) in [2, 3]:
        task_type = 'regression'
    elif options is None:
        task_type = 'captioning'
    else:
        raise Exception('Invalid options')

    buttons = []

    if task_type == 'classification':
        use_dropdown = len(options) > 5

        if use_dropdown:
            dd = Dropdown(options=options)
            display(dd)
            btn = Button(description='submit')
            def on_click(btn):
                add_annotation(dd.value)
            btn.on_click(on_click)
            buttons.append(btn)

        else:
            for label in options:
                btn = Button(description=label)
                def on_click(label, btn):
                    add_annotation(label)
                btn.on_click(functools.partial(on_click, label))
                buttons.append(btn)

    elif task_type == 'regression':
        target_type = type(options[0])
        if target_type == int:
            cls = IntSlider
        else:
            cls = FloatSlider
        if len(options) == 2:
            min_val, max_val = options
            slider = cls(min=min_val, max=max_val)
        else:
            min_val, max_val, step_val = options
            slider = cls(min=min_val, max=max_val, step=step_val)
        display(slider)
        btn = Button(description='submit')
        def on_click(btn):
            add_annotation(slider.value)
        btn.on_click(on_click)
        buttons.append(btn)

    else:
        ta = Textarea()
        display(ta)
        btn = Button(description='submit')
        def on_click(btn):
            add_annotation(ta.value)
        btn.on_click(on_click)
        buttons.append(btn)

    if include_skip:
        btn = Button(description='skip')
        btn.on_click(skip)
        buttons.append(btn)

    box = HBox(buttons)
    display(box)

    out = Output()
    display(out)

    show_next()

    return annotations


def multi_label_annotate(examples, options=None, shuffle=False, display_fn=display):
    """
    Build an interactive widget for annotating a list of input examples.

    Parameters
    ----------
    examples: list(any), list of items to annotate
    options: Dict
        dictionary of category names and category classes
        ex {'gender':['male', 'female', 'unisex']}
    shuffle: bool, shuffle the examples before annotating
    display_fn: func, function for displaying an example to the user

    Returns
    -------
    annotations : defaultdict of dicts, dict of annotated examples
        (example, {task:[label... label],task2:[label]})
    """
    examples = list(examples)
    if shuffle:
        random.shuffle(examples)

    annotation_dict = defaultdict(dict)
    all_buttons = []

    current_index = -1

    def set_label_text():
        nonlocal count_label
        if current_index < len(examples):
            count_label.value = (
                '{} examples annotated, {} examples left<br>Asset name: <code>{}</code><hr>'.format(
                    len(annotation_dict), len(examples) - current_index, examples[current_index]
                )
            )
        else:
            count_label.value = '{} examples annotated, {} examples left<br>Annoation done.<hr>'.format(
                len(annotation_dict), len(examples) - current_index
            )

    def show_next():
        clear_colors()
        nonlocal current_index
        current_index += 1
        set_label_text()
        if current_index >= len(examples):
            for btn in buttons:
                btn.disabled = True
            with out:
                clear_output()
            return
        with out:
            clear_output(wait=True)
            display_fn(examples[current_index])

    def go_back():
        clear_colors()
        nonlocal current_index
        current_index -= 1
        if current_index < 0:
            print('cannot go back')
            return
        with out:
            clear_output(wait=True)
            try:
                del annotation_dict[examples[current_index]]
                set_label_text()
                display_fn(examples[current_index])
            except KeyError:
                print("Key 'testing' not found")

    def del_current_annotation():
        nonlocal current_index
        with out:
            clear_output(wait=True)
            display_fn(examples[current_index])
            del annotation_dict[examples[current_index]]
        current_index -= 1
        show_next()

    def add_annotation(annotation_dict, annotation, task_name):
        if task_name not in annotation_dict[examples[current_index]].keys():
            annotation_dict[examples[current_index]][task_name] = [annotation]
        else:
            # check if the annotation is already in the `annotation_dict`, if so, that means
            # it has been clicked a second time, and we should remove both the color and
            # the annotation
            if annotation in annotation_dict[examples[current_index]][task_name]:
                annotation_dict[examples[current_index]][task_name].remove(annotation)
            else:
                annotation_dict[examples[current_index]][task_name].append(annotation)

    def skip(btn):
        show_next()

    def done(btn):
        show_next()

    def back(btn):
        go_back()

    def clear_annotation(btn):
        del_current_annotation()

    def clear_colors():
        nonlocal all_buttons
        for button in all_buttons:
            try:
                button.style.button_color = None
            except Exception:
                continue

    count_label = HTML()
    set_label_text()
    display(count_label)

    if type(options) == dict:
        task_type = 'classification'
    else:
        raise ValueError('Invalid options. Must be classification dictionary.')

    if task_type == 'classification':
        for key, value in options.items():
            buttons = []
            print(key)
            for label in value:
                btn = MultiLabelButton(description=label, task_name=key)

                def on_click(label, task_name, btn):
                    # if button has a color, clear it! if not, give it a color!
                    if btn.style.button_color is None:
                        btn.style.button_color = 'lightgreen'
                    else:
                        btn.style.button_color = None
                    add_annotation(annotation_dict, label, task_name)

                btn.button.on_click(functools.partial(on_click, label, btn.task_name))
                buttons.append(btn.button)
                all_buttons.append(btn.button)

            box = HBox(buttons)
            display(box)

    print('')
    buttons = []

    btn = Button(description='done')
    btn.on_click(skip)
    buttons.append(btn)

    btn = Button(description='back')
    btn.on_click(back)
    buttons.append(btn)

    btn = Button(description='clear current')
    btn.on_click(clear_annotation)
    buttons.append(btn)

    btn = Button(description='skip')
    btn.on_click(skip)
    buttons.append(btn)

    all_buttons += buttons

    box = HBox(buttons)
    display(box)

    out = Output()
    display(out)

    show_next()

    return annotation_dict


class MultiLabelButton(object):
    def __init__(self, description, task_name):
        self.description = description
        self.task_name = task_name
        self.button = Button(description=description)
