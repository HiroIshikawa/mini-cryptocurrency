
    <ul>
        <li>node type:    <br>     {{node_data.type}}</li>
        <li>pub_key:      <br>     {{node_data.pub_key}}</li>
        <li>mempool:      <br>     
            <ul>
                {% for trx in node_data.mempool %}
                    <li>{{trx}}</li>
                {% endfor %}
            </ul>
        </li>
        {% if 'blockchain' in node_data %}
            {% if node_data.blockchain %}
                <li>blockchain
                    <ul>
                        <li>length: {{node_data.blockchain.length}}</li>
                        <!-- <li>blocks: {{node_data.blockchain.blocks}}</li> -->
                        <li> blocks:
                            <ul>
                                 {% for block in node_data.blockchain.blocks %}
                                    <li>block:
                                        <ul>
                                            {% for key, val in block.items() %}
                                                {% if key == 'trxs_map' %}
                                                    <li>trx:
                                                        <ul>
                                                            {% for trx in val %}
                                                                <li>{{trx}}</li>
                                                            {% endfor %}
                                                        </ul>
                                                    </li>
                                                {% else %}
                                                    <li>{{key}} {{val}}</li>
                                                {% endif %}
                                            {% endfor %}
                                        </ul>
                                    </li>
                                 {% endfor %}
                            </ul>
                        </li>
                    </ul>
                </li>
            {% endif %}
        {% endif %}
    </ul>
