
@app.route('/editar_categorias/<int:id>', methods=['GET', 'POST'])
def editar_categorias(id):
   if 'id_usuario' not in session:
       flash('Precisa estar logado')
       return redirect(url_for('login'))

   cursor = con.cursor()

   try:
       cursor.execute("""
           SELECT NOME, STATUS, cor, icone
           FROM CATEGORIA
           WHERE ID_CATEGORIA = ?
             AND ID_USUARIO = ?
       """, (id, session['id_usuario']))

       categoria = cursor.fetchone()

       if categoria is None:
           flash('Categoria não encontrada!')
           return redirect(url_for('listar_categorias'))

       if id in [1001, 1002]:
           flash('Esta categoria não pode ser editada.')
           return redirect(url_for('listar_categorias'))


       if request.method == 'POST':
           nome_categoria = request.form['nome_categoria']
           nome_categoria.strip().lower()
           cor = request.form['cor']
           icone = request.form['icone']

           if not nome_categoria:
               flash('Informe o nome da categoria!')
               nome = buscarUsuario(session['id_usuario'])[1]
               usuario = buscarUsuario(id)
               caminho = "img/capas/" + str(usuario[0]) + ".jpg"

               return render_template(
                   'editar_categorias.html',
                   id=id,
                   nome=nome,
                   categoria=categoria,
                   img=caminho
               )

           cursor.execute("""
               SELECT 1
               FROM CATEGORIA
               WHERE LOWER(NOME) = ? 
                 AND ID_CATEGORIA != ?
                 AND ID_USUARIO = ?
           """, (nome_categoria, id, session['id_usuario']))

           if cursor.fetchone() is not None:
               flash('Erro: Categoria já cadastrada!')
               nome = buscarUsuario(session['id_usuario'])[1]
               usuario = buscarUsuario(id)
               caminho = "img/capas/" + str(usuario[0]) + ".jpg"
               return render_template(
                   'editar_categorias.html',
                   id=id,
                   nome=nome,
                   categoria=(nome_categoria, categoria[1]),
                   img=caminho
               )

           cursor.execute("""
               UPDATE CATEGORIA
               SET NOME = ?,
                   COR = ?,
                   ICONE = ?
               WHERE ID_CATEGORIA = ?
                 AND ID_USUARIO = ?
           """, (
               nome_categoria,
               cor,
               icone,
               id,
               session['id_usuario']
           ))

           con.commit()
           flash('Categoria editada com sucesso!')
           return redirect(url_for('listar_categorias'))

       nome = buscarUsuario(session['id_usuario'])[1]
       usuario = buscarUsuario(id)
       caminho = "img/capas/" + str(usuario[0]) + ".jpg"

       return render_template(
           'editar_categorias.html',
           id=id,
           nome=nome,
           categoria=categoria,
           img=caminho
       )

   except Exception as e:
       con.rollback()
       flash(f'Ocorreu um erro: {e}')
       return redirect(url_for('listar_categorias'))

   finally:
       cursor.close()
