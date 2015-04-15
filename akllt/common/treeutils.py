def create_tree(parent, tree, refs=()):
    """Creates tree in database by given list of nested lists of tree nodes.

    This functions accepts list of nested lists [1] and creates database
    records, maintaining given tree structure.

    Parameters:
    - parent: treebeard.models.Node, parent node for the tree to build on.
    - tree: list of lists with treebeard.models.Node instances.
    - refs: tuple, used for internaly for protection against endless recursion.

    Returns: None

    [1] https://docs.djangoproject.com/en/1.8/ref/templates/builtins/#unordered-list

    """
    child = None
    refs += (id(tree),)
    for node in tree:
        if isinstance(node, list):
            if id(node) not in refs:
                create_tree(child, node, refs=refs)
        else:
            child = parent.add_child(instance=node)


def grow_tree_iter(tree, dfs_tree):
    """Iterator over dfs_tree.

    Usually you should use this generator like this:

        >>> from wagtail.wagtailcore.models import Page
        >>> dfs_tree = [
        ...     Page(slug='a', numchild=2),
        ...     Page(slug='b', numchild=0),
        ...     Page(slug='c', numchild=1),
        ...     Page(slug='d', numchild=0),
        ...     Page(slug='e', numchild=0),
        ...     Page(slug='f', numchild=1),
        ...     Page(slug='g', numchild=0),
        ... ]
        >>> tree = []
        >>> for children, node in grow_tree_iter(tree, dfs_tree):
        ...     children.append(node.slug)
        >>> tree
        ['a', ['b', 'c', ['d']], 'e', 'f', ['g']]

    You can get dfs_tree using treebeard.models.Node.get_descendants method.

    Parameters:
    - tree: empty list, this list will be populated with nodes.
    - dfs_tree: list of nodes ordered as DFS (Depth-first search) [1].

    Returns: generator

    [1] http://en.wikipedia.org/wiki/Depth-first_search

    """
    stack = [(tree, 0)]
    for node in dfs_tree:
        children, children_count = stack[-1]
        children_count = node.get_children_count()

        yield children, node

        if children_count > 0:
            children.append([])
            stack.append((children[-1], children_count))
        else:
            while children_count <= 1 and stack:
                children, children_count = stack.pop()
            stack.append((children, children_count - 1))


def grow_tree(dfs_tree, callback=(lambda node: node)):
    """Takes flat tree and grows tree composed of nested lists.

    Parameters:
    - tree: empty list, this wilst will be populated with nodes.
    - dfs_tree: list of nodes ordered as DFS (Depth-first search) [1].

    Returns: list of nested lists [2] containing flat tree nodes.

    [1] http://en.wikipedia.org/wiki/Depth-first_search
    [2] https://docs.djangoproject.com/en/1.8/ref/templates/builtins/#unordered-list

    """
    tree = []
    for children, node in grow_tree_iter(tree, dfs_tree):
        children.append(callback(node))
    return tree


def transform(tree):
    """Transform list of lists to list of tuples containing item and children.

    It actually transforms ``[a, [b]]`` to ``[(a, [(b, [])])]``. This
    transformed structure is more convinient to use in recursive functions.
    While input tree is more convinient to write.

    Parameters:
    - tree: list of lists

    Returns: lists of tuples containing item and children.

    """
    result = []
    for node in tree:
        if isinstance(node, list):
            result[-1] = (result[-1][0], transform(node))
        else:
            result.append((node, []))
    return result
