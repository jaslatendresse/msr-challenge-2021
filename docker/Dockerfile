FROM pandoc/ubuntu-latex
RUN apt-get update
RUN apt-get install -y texlive-latex-extra
RUN tlmgr update --self
RUN tlmgr install adjustbox babel-german background bidi collectbox csquotes everypage filehook footmisc footnotebackref framed fvextra letltxmacro ly1 mdframed multirow mweights needspace pagecolor sourcecodepro sourcesanspro titling ucharcat ulem unicode-math upquote xecjk xurl zref
ENTRYPOINT ["/bin/sh", "-c"]
