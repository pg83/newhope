def construct_pt_app():
    from prompt_toolkit.application import Application
    from prompt_toolkit.key_binding import KeyBindings, merge_key_bindings
    from prompt_toolkit.key_binding.defaults import load_key_bindings
    from prompt_toolkit.layout import Layout, VSplit, HSplit, Window
    from prompt_toolkit.layout.controls import FormattedTextControl
    from prompt_toolkit.styles import Style
    from prompt_toolkit.widgets import TextArea, VerticalLine

    text_area_1 = TextArea()
    text_area_2 = TextArea()
    
    application = Application(
        layout=Layout(
            container=HSplit([
                VSplit([text_area_1, VerticalLine(), text_area_2]),
                Window(height=1, style='class:title', content=FormattedTextControl('text')),
            ]),
        ),
        full_screen=True,
        mouse_support=True,
    )

    def write(t):
        text_area_1.buffer.insert_text(t)

    y.log_stream.write = write
        
    def run_f():
        y.asyncio.set_event_loop(y.asyncio.new_event_loop())
        application.run()
    
    y.threading.Thread(target=run_f).start()

    def on_build_result(arg):
        pass

    return on_build_result
